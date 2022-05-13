import googletrans as gtrans
from tqdm.auto import tqdm

# Translating text columns to english
# works google translator version 4.0.0rci
# installable via following command
#       pip install googletrans==4.0.0rc1

def translate_column(df, column_name, new_column_name, from_lang='nl', to_lang='en'):
    nl_to_eng = gtrans.Translator()
    df[new_column_name] = df[column_name].fillna('Missing').astype('str')

    original_texts = []
    translated_texts = []

    for text_element in tqdm(df[new_column_name].unique()):
        original_texts.append(text_element)
        translated_texts.append(nl_to_eng.translate(text_element,src=from_lang, dest=to_lang).text)

    for i in tqdm(range(0,len(original_texts))):
        df.loc[df[new_column_name]==original_texts[i],'trans_origin'] = translated_texts[i]

    return df