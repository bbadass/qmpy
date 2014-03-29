import logging

from renderable import *
import qmpy
import point

logger = logging.getLogger(__name__)

class Text(Renderable):
    def __init__(self, pt, text, **kwargs):
        self.point = point.Point(pt)
        self.text = text
        self.options = {'ha':'left', 'va':'top'}
        #if self.point.coord[0] == 0:
        #    self.options['va'] = 'bottom'
        #if self.point.coord[1] == 1:
        #    self.options['ha'] = 'right'
        self.options.update(kwargs)

    @property
    def dim(self):
        return self.point.dim

    def draw_in_matplotlib(self, **kwargs):
        plt.text(self.point.coord[0],
                 self.point.coord[1], self.text, **kwargs)

    def get_flot_series(self, **kwargs):
        cmd = '\no = plot.pointOffset({{ x: {x}, y: {y} }});'.format(
                x=self.point.coord[0], y=self.point.coord[1])

        opts = {}
        if self.options['va'] == 'top':
            opts['top'] = '"+( o.top )+"px'
        elif self.options['va'] == 'bottom':
            opts['bottom'] = '"+( o.top )+"px'

        if self.options['ha'] == 'left':
            opts['left'] = '"+( o.left )+"px'
        elif self.options['ha'] == 'right':
            opts['right'] = '"+( o.left )+"px'
            
        opts['position'] = 'absolute'

        opts = ';'.join(['%s:%s' % (k, v) for k, v in opts.items() ])
        div = '<div style={options}>{string}</div>'
        div = div.format(string=self.text, options=opts)

        cmd += '\nplaceholder.append("{div}");'.format(div=div)
        return cmd