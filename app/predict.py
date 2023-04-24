from typing import Dict, List
from util import clean_text
import pickle


CRITERIAS = {
    1:"A política específica claramente quais dados são coletados?",
    2: "A Política de Privacidade específica claramente como a empresa pode usar os dados coletados?",
    3: "A política trata questões relacionadas à privacidade de crianças?",
    4: "A Política específica claramente como os dados são coletados?",
    5: "A Política de Privacidade claramente especifica se as informações podem ser compartilhadas ou vendidas para terceiros?",
    6: "Decisões Automatizadas",
    7: "A Política de Privacidade claramente especifica quais são as medidas adotadas pela aplicação para garantir a confidencialidade, a integridade e a qualidade dos dados?",
    8: "A política explica claramente o que acontece com os dados do usuário caso ele exclua a conta?",
    9: "A Política de Privacidade claramente especifica os direitos do usuário?",
    10: "A Política de Privacidade fala sobre como ela utiliza cookie no seu site?",
    11: "A Política de Privacidade claramente informa dados para contato com a empresa?",
    12: "A Política de Privacidade claramente específica como os dados são armazenados?",
    13: "A Política de Privacidade fala sobre transferir dados do usuário em nível internacional?",
    14: "Como as alterações nas políticas são tratadas?"
}

model = pickle.load(open('model.sav', 'rb'))
vectorizer = pickle.load(open('vectorizer.pickle', 'rb'))

INFO_NOT_FOUND = "Critério nāo encontrado"


def predict(headers: List[str])-> Dict:
    clean_headers = list(map(clean_text , headers))

    vectorized_headers = vectorizer.transform(clean_headers)
    prediction = model.predict(vectorized_headers)

    print(clean_headers)
    print(prediction)

    agg_predictions = {}
    for i in CRITERIAS:
        agg_predictions[i] = []

    for i, prediction in enumerate(prediction):
        if prediction!= 0:
            agg_predictions[prediction].append(headers[i])
    
    formated_dict = {}
    for (key, value) in agg_predictions.items():
        criteria = CRITERIAS[key]
        formated_dict[criteria] = ",".join(value) if len(value) != 0 else INFO_NOT_FOUND

    return formated_dict

    



