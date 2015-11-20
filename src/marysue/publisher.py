"""High-level orchestration of the writing of the novel."""

import os
import sys
from tempfile import mkstemp

import marysue.util as random
from marysue.util import capitalize, log
from marysue.editor import edit_story
from marysue.proofreader import proofread, word_count


class Novel(object):
    front_matter = """\
# A Time for Destiny

### The Illustrious Career of Serenity Starlight Warhammer O'James during her First Three Years in the Space Fighters

_SPACE SURGEON GENERALS WARNING:_ THE SPACE SURGEON GENERAL HAS DETERMINED THAT
EXPOSURE TO LARGE AMOUNTS OF COMPUTER-GENERATED FICTION MAY CAUSE HEADACHES,
DIZZINESS, NAUSEA, AND AN ACUTE DESIRE TO SKIP AROUND TO FIND THE GOOD BITS.

FOR YOUR OWN WELL-BEING, DO NOT EXCEED THE RECOMMENDED MAXIMUM INTAKE OF 2 (TWO)
CHAPTERS IN ANY 48 (FORTY EIGHT) HOUR PERIOD.

"""

    def __init__(self, chapters, generate_front_matter=True, synopsis=False, dump=False):
        self.chapters = chapters
        self.generate_front_matter = generate_front_matter
        self.synopsis = synopsis
        self.dump = dump

        self.text = ''
        self.used_titles = set()
        self.introduced = set()

    def suggest_title_objects(self, plot, objects=None):
        from marysue.plot import Kidnapping, LoseItem, Vanquished

        if objects is None:
            objects = set()
        if isinstance(plot, Kidnapping):
            objects.add(plot.subject)
        if isinstance(plot, (LoseItem, Vanquished)):
            objects.add(plot.object)
        for child in plot:
            self.suggest_title_objects(child, objects=objects)    
        return objects

    def pick_title(self, plot):
        titles = [o.definite for o in self.suggest_title_objects(plot)]
        if not titles:
            titles = ['The Destiny of Fate']
        base_title = capitalize(random.choice(tuple(titles)))
        prefixes = [
            'The Return of ',
            'The Revenge of ',
            'The Scourge of ',
            'The Menace of ',
            'The Secret of ',
            'The Time of ',
            'The Scourge of ',
            'The Mystery of ',
            'The Phantom of ',
        ]
        multipref = []
        for a in prefixes:
            for b in prefixes:
                multipref.append(a + b)
        prefixes.extend(multipref)
    
        title = base_title
        while title in self.used_titles:
            title = prefixes.pop(0) + base_title
        self.used_titles.add(title)

        return title

    def generate_chapter(self, n, plotter, **kwargs):
        ### tell the plotter to give us an acceptable plot ###

        plot = plotter.generate_acceptable_plot(**kwargs)

        ### dump the synopsis, if requested ###

        if self.synopsis:
            plot.print_synopsis()
            sys.exit(0)

        ### write a story around the plot, then edit it ###

        story = plotter.plot_to_story(plot)

        story = edit_story(story, self.introduced, **kwargs)

        ### dump the story, if requested ###

        if self.dump:
            story.dump(sys.stdout)
            sys.exit(0)

        ### give the thing a title that hasn't been used yet ###

        self.chapters[n]['commuted_plots'] = plotter.commuted_plots
        self.chapters[n]['plot'] = plot
        self.chapters[n]['title'] = self.pick_title(plot)

        ### install it in the chapters ###

        text = story.render()
        text = proofread(text)

        self.chapters[n]['text'] = text
        self.chapters[n]['word_count'] = word_count(text)

    def assemble_novel_text(self):
        self.text = ''

        # [WHARRGARBL](http://i1.kym-cdn.com/photos/images/newsfeed/000/032/388/wharrgarbl.jpg).

        if self.generate_front_matter:
            self.text += self.front_matter
            self.text += '\n\n## Contents\n\n'
            self.text += '<a name="contents"></a>\n\n'
            for n, chapter in enumerate(self.chapters):
                self.text += '1. [%s](#%s)  \n' % (chapter['title'], n)
            self.text += '\n\n'

        for n, chapter in enumerate(self.chapters):
            self.text += (
                ('<a name="%s"></a>\n\n' % n) +
                ('## %s. %s' % (n+1, chapter['title'])) +
                #('(%s)' % chapter['commuted_plots']) +
                '\n\n' +
                chapter['text'] +
                '\n\n'
            )
            #self.text += '[Up to Table of Contents](#contents)\n\n'

    def trim(self):
        ### trim the novel to reasonable length ###
        
        # Note: this isn't perfect, because every time we cut a chapter,
        # we make the table of contents shorter too.  But, it's usually OK.
        # The total number of words outside of any chapter is usually around 500.
        
        done = False
        while not done:
            self.assemble_novel_text()
            self.novel_wc = word_count(self.text)
            overrun = self.novel_wc - 50000
            could_be_cut = [(n, c) for (n, c) in enumerate(self.chapters) if c['word_count'] < overrun and c['position'] == 'middle']
            could_be_cut.sort(key=lambda pair: pair[1]['word_count'])
            if could_be_cut:
                n, chapter = could_be_cut[0]
                log('cutting:', n, chapter['title'], chapter['word_count'])
                self.chapters.remove(chapter)
            else:
                done = True

        self.total_wc = sum([chapter['word_count'] for chapter in self.chapters])
        self.avg_wc = (self.total_wc * 1.0) / (len(self.chapters) * 1.0)

        self.retitle_chapters()
        self.assemble_novel_text()
        self.novel_wc = word_count(self.text)

        for n, c in enumerate(self.chapters):
            if c['commuted_plots']:
                log(n+1, c['commuted_plots'])

    def retitle_chapters(self):
        self.used_titles = set()
        for n, c in enumerate(self.chapters):
            c['title'] = self.pick_title(c['plot'])

    def publish(self):
        fd, temp_filename = mkstemp(suffix='.md')
        os.close(fd)
        with open(temp_filename, 'w') as f:
            f.write(self.text)
            f.write("## word counts for this novel\n\n")
            for n, chapter in enumerate(self.chapters):
                f.write("Chapter %02d: %s  \n" % (n + 1, chapter['word_count']))
            f.write("Chapter total: %0.2d  \n" % self.total_wc)
            f.write("Average: %0.2d  \n" % self.avg_wc)
            f.write("Entire Novel: %s  \n" % self.novel_wc)
        log(temp_filename)
        html_filename = 'temp.html'
        output_filename = 'Serenity_Starlight.html'
        os.system("pandoc --from=markdown --to=html5 --css=marysue.css <%s >%s" % (temp_filename, html_filename))
        with open(html_filename, 'r') as f_in:
            with open(output_filename, 'w') as f_out:
                for line in f_in:
                    if 'rel="stylesheet"' in line:
                        f_out.write('<style type="text/css">\n')
                        f_out.write(open('marysue.css', 'r').read())
                        f_out.write('</style>\n')
                    else:
                        f_out.write(line)
        os.system("firefox %s &" % output_filename)
