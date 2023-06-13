from models import Translation
from transformers import T5Tokenizer, T5ForConditionalGeneration

#t5-base t5-large
tokenizer = T5Tokenizer.from_pretrained('t5-small', model_max_length=512)
translator = T5ForConditionalGeneration.from_pretrained('t5-small')

## store translation
## Translation request and save to database
def store_translation(t):
    model = TranslationModel(text=t.text, base_lang=t.base_lang, final_lang=t.final_lang)
    model.save()
    return model.id

## run translation
## Run a pretrained deep learning model to translate the text
def run_translation(t_id: int):
    model = TranslationModel.get_by_id(t_id)

    prefix = f"translate {model.text} from {model.base_lang} to {model.final_lang}: "
    input_ids = tokenizer(prefix, return_tensors="pt").input_ids

    outputs = translator.generate(input_ids, max_new_tokens=512)
    translation = tokenizer.decode(outputs[0], skip_special_tokens=True)
    model.translation = translation
    model.save()



## find_translation 
## retrieve  translation from database
def find_translation(t_id: int):
    model = TranslationModel.get_by_id(t_id)
    Translation = model.translation
    if translation is None:
        translation = "Translation in progress"
    return translation