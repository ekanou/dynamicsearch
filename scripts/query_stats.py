import xml.etree.ElementTree
from xml.etree.ElementTree import iterparse


class Interaction(object):


    def __init__(self, session_id, topic_id, interaction_id, query, result_list, clicked_list):

        self.session_id = session_id
        self.topic_id = topic_id
        self.interaction_id = interaction_id
        self.query = query
        self.result_list = result_list
        self.clicked_list = clicked_list


def load_session_logs(session_logs):

    session_id = -1
    topic_id = -1
    interaction_id = -1
    query = ''
    clicked_list = []
    result_list = []
    num_interactions = 0
    queryToInteractionMap = {}

    e = xml.etree.ElementTree.parse(session_logs).getroot()

    #query_stats_file = open('query_stats2.txt', 'w')

    for ses in e.iter('session'):
        session_id = ses.attrib.get('num')
        for topic in ses.iter('topic'):
            topic_id = topic.attrib.get('num')
        for inter in ses.iter('interaction'):

            interaction_id = inter.attrib.get('num')
            clicked_list = []
            result_list = []

            for query in inter.iter('query'):
                query = query.text

            for results_node in inter.iter('results'):
                result_list = [r.text for r in results_node.iter('clueweb12id') ]
            for clicked_node in inter.iter('clicked'):
                clicked_list = [r.text for r in clicked_node.iter('docno')]

            interaction_loaded = Interaction(session_id, topic_id, interaction_id, query, result_list, clicked_list)
            if query in queryToInteractionMap.keys():
                queryToInteractionMap[query].append(interaction_loaded)
            else:
                queryToInteractionMap[query] = [interaction_loaded]

            num_interactions += 1

            #print >> query_stats_file, session_id, topic_id, interaction_id, query, str(result_list), str(clicked_list)


    return queryToInteractionMap

def load_judgements(judgements_file_path):

    relevance_map = {}
    for line in open(judgements_file_path):
        line_parts = line.strip().split()
        topic_id = line_parts[0]
        doc_id = line_parts[2]
        rel_value = line_parts[3]
        relevance_map[ topic_id + '_' + doc_id] = int(rel_value)
    return relevance_map

def is_doc_rel_to_topic(relevance_map, doc_id, topic_id):

    return relevance_map.get(topic_id + '_' + doc_id) >= 1

if __name__ == '__main__':

    data_home = './../sessions2014/'

    session_logs = data_home + '/sessiontrack2014.xml'
    judgements = data_home + '/judgments.txt'

    relevance_map = load_judgements(judgements)
    query_to_interaction_map = load_session_logs(session_logs)

    seperator = ';'
    query_stats_file = open(data_home + 'query_stats.csv', 'w')
    line_for_query = ''

    columns = ['Query', '#issued', '#clicks', '#clicks_on_relevant_items', '#relevant_items_in_top_10', 'topic_id']
    print >> query_stats_file, seperator.join(columns)

    for q in query_to_interaction_map.keys():

        interaction_list_for_q = query_to_interaction_map[q]
        num_issued = len(interaction_list_for_q)
        num_clicks = 0
        num_clicks_on_rel = 0
        num_rel_in_top_10 = 0

        for interaction in interaction_list_for_q:
            topic_id = interaction.topic_id
            num_clicks += len(interaction.clicked_list)
            num_clicks_on_rel += [is_doc_rel_to_topic(relevance_map, doc_id, topic_id) for doc_id in interaction.clicked_list].count(True)
            #print interaction.result_list
            num_rel_in_top_10 += [is_doc_rel_to_topic(relevance_map, doc_id, topic_id) for doc_id in interaction.result_list].count(True)
        columns_for_query = [q, str(num_issued) , str(num_clicks), str(num_clicks_on_rel), str(num_rel_in_top_10)]

        print >> query_stats_file, seperator.join(columns_for_query) + seperator + topic_id





