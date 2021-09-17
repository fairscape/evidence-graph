class LocalEG:
    '''
    Local Evidence Graph shows once level of depth
    '''
    def __init__(self,id,token = None):
        '''
        id to create local evidence graph for
        '''
        meta = retrieve_metadata(id,token)
        self.json_eg = remove_non_evidence(meta)


############
# add depth option
############
class EG:
    '''
    Full evidence graph tracking all proveance related to given identifier
    '''
    def __init__(self,id,token = None):

        self.id, self.token = id, token
        self.local_eg = LocalEG(id,token)

    def expand(self):
        json_eg = self.local_eg.json_eg

        for key in json_eg.keys():

            #find all previous steps to look to expand
            if isinstance(json_eg[key],dict):
                #confirm next step down as identifier
                if '@id' not in json_eg[key].keys():
                    continue
                json_eg[key] = expand_evidence(json_eg[key]['@id'],self.token)

            #look through lists for more things to expand
            if isinstance(json_eg[key],list):
                for i in range(len(json_eg[key])):
                    item = json_eg[key][i]

                    if isinstance(item,dict):
                        if '@id' not in item.keys():
                            continue

                        json_eg[key][i] = expand_evidence(item['@id'],self.token)

        self.eg = json_eg
