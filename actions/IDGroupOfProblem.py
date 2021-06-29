

def IDOfgroup(class_name):
    dictClass = {'Other':'301',
                  'SIS':'1807',
                  'blackboard':'1850',
                  'helpdesk_support':'6001',
                  'learning_tech_resource':'6002',
                  'main_gate_university':'7801',
                  'maward':'1805',
                  'network_security':'6301',
                  'scientific_research_system':'1816',
                  'systems_infrastructure_apps':'6304',
                  'telephone_conferences':'6303',
                  'transaction_flow_system':'1811'}
    id_group = dictClass[class_name]
    return id_group


# print(IDOfgroup('maward'))