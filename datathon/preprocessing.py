import googletrans as gtrans
import numpy as np
from tqdm.auto import tqdm


def translate_column(df, column_name, new_column_name, from_lang='nl', to_lang='en'):
    '''
    Add a column with translated text to pandas.DataFrame. 
    Works google translator version 4.0.0rci (pip install googletrans==4.0.0rc1).

    Arguments:
        df [pandas.DataFrame]
        column_name [str]: column with to-be-translated text
        new_column_name [str]: column to store translated text
        from_lang [str]: to-be-translated text language
        to_lang [str]: target language
    '''
    nl_to_eng = gtrans.Translator()
    df[new_column_name] = df[column_name].fillna('Missing').astype('str')
    original_texts = []
    translated_texts = []
    for text_element in tqdm(df[new_column_name].unique()):
        original_texts.append(text_element)
        translated_texts.append(nl_to_eng.translate(text_element,src=from_lang, dest=to_lang).text)

    for i in tqdm(range(0,len(original_texts))):
        df.loc[df[new_column_name]==original_texts[i], new_column_name] = translated_texts[i]
    return df


def make_table(df, column_names, MultiIndex=False):
    '''
    Returns DataFrame with structure similar to R _table_ function.

    Arguments:
        df [pandas.DataFrame]: input DataFrame
        column_names [str]: ordered list of columns for group splitting
    '''
    table = df.groupby(column_names).size().to_frame('size')
    if not MultiIndex:
        levels = list(np.arange(len(column_names)))
        table = table.reset_index(level=levels)
    return table


