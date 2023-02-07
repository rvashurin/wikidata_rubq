import datasets
import os
import json

_DESCRIPTION = """\
HuggingFace wrapper for https://github.com/vladislavneon/RuBQ dataset
"""

_HOMEPAGE = "https://zenodo.org/record/4345697#.Y01k81JBy3I"


_LICENSE = "Attribution-ShareAlike 4.0 International"

_LANGS = ["ru","en"]


_URLS = {
    "test": "https://raw.githubusercontent.com/vladislavneon/RuBQ/master/RuBQ_2.0/RuBQ_2.0_test.json",  
    "dev": "https://raw.githubusercontent.com/vladislavneon/RuBQ/master/RuBQ_2.0/RuBQ_2.0_dev.json",
}


_DATA_DIRECTORY = "."
VERSION = datasets.Version("0.0.1")


class WikidataRuBQConfig(datasets.BuilderConfig):
    """BuilderConfig for WikidataRuBQ."""

    def __init__(self, **kwargs):
        """BuilderConfig for WikidataRuBQ.
        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super(WikidataRuBQConfig, self).__init__(**kwargs)
        
        
class WikidataRuBQ(datasets.GeneratorBasedBuilder):
    """HuggingFace wrapper https://github.com/vladislavneon/RuBQ/tree/master/RuBQ_2.0 dataset"""

    BUILDER_CONFIG_CLASS = WikidataRuBQConfig
    BUILDER_CONFIGS = []
    BUILDER_CONFIGS += [
        WikidataRuBQConfig(
            name=f"multiple_{ln}",
            version=VERSION,
            description="questions with russian multiple labels as answers",
        )
        for ln in _LANGS
    ]

    DEFAULT_CONFIG_NAME = "multiple_en"

    def _info(self):
        features = datasets.Features(
            {
                "object": datasets.Sequence(datasets.Value("string")),
                "question": datasets.Value("string")
            }
        )

        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            homepage=_HOMEPAGE,
            license=_LICENSE,
        )
    
    def _split_generators(self, dl_manager):
        if self.config.name == "default":
            version, lang = "multiple", "en"
        else:
            version, lang = self.config.name.split("_")   

        if lang not in _LANGS:
            raise ValueError(f"Language {lang} not supported")
            
        downloaded_files = dl_manager.download_and_extract(_URLS)

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "filepath": downloaded_files["dev"],
                    "lang": lang,
                }),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "filepath": downloaded_files["dev"],
                    "lang": lang,
                }),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "filepath": downloaded_files["test"],
                    "lang": lang,
                })
        ]
    
    def _generate_examples(self, filepath, lang):

        with open(filepath, encoding="utf-8") as f:
            item = json.load(f)
            for i in item:
                question = i['question_text'] if lang == 'ru' else i['question_eng']

                objects = list(set(
                    [answer['value'].split('entity/')[1] for answer in i['answers'] if '/Q' in answer['value']]
                ))

                key = i['uid']
                if len(set(objects)) >= 1:
                    yield (key,
                        {
                            "object": objects,
                            "question": question,
                        }
                    )
