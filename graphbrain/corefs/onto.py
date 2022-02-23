from graphbrain.corefs import make_corefs
from graphbrain.utils.ontology import subtypes


class CorefsOnto:
    def __init__(self, hg, sequence=None):
        self.hg = hg
        self.sequence = sequence
        self.corefs = 0
        self.done = set()

    def process_edge(self, edge):
        if edge.type()[0] == 'C' and edge not in self.done:
            self.done.add(edge)

            subs = tuple(subtypes(self.hg, edge))

            # check if the concept should be assigned to a synonym set
            if len(subs) > 0:
                # find set with the highest degree and normalize set
                # degrees by total degree
                sub_degs = [self.hg.deep_degree(sub) for sub in subs]
                total_deg = sum(sub_degs)
                total_deg = 1 if total_deg == 0 else total_deg
                sub_ratios = [sub_deg / total_deg for sub_deg in sub_degs]
                max_ratio = 0.
                best_pos = -1
                for pos, ratio in enumerate(sub_ratios):
                    if ratio > max_ratio:
                        max_ratio = ratio
                        best_pos = pos

                # compute some degree-related metrics
                sdd = self.hg.deep_degree(subs[best_pos])
                dd = self.hg.deep_degree(edge)

                if dd > sdd:
                    sdd_dd = float(sdd) / float(dd)

                    self.logger.debug('concept: {}'.format(edge.to_str()))
                    self.logger.debug('subconcepts: {}'.format(subs))
                    self.logger.debug('# subs: {}'.format(len(subs)))
                    self.logger.debug('max_ratio: {}'.format(max_ratio))
                    self.logger.debug('sdd: {}'.format(sdd))
                    self.logger.debug('dd: {}'.format(dd))
                    self.logger.debug('sdd_dd: {}'.format(sdd_dd))

                    if max_ratio >= .7:  # and sdd_dd < .5:
                        edge1 = edge
                        edge2 = subs[best_pos]

                        self.logger.debug(
                            'are corefs: {} | {}'.format(edge1.to_str(),
                                                         edge2.to_str()))

                        self.corefs += 1
                        make_corefs(self.hg, edge1, edge2)

    def run(self):
        print('processing edges...')
        if self.sequence is None:
            for edge in self.hg.all():
                self.process_edge(edge)
        else:
            for edge in self.hg.sequence(self.sequence):
                self.process_edge(edge)
        print('{} coreferences were added.'.format(str(self.corefs)))
