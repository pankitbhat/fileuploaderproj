from haystack import indexes
from .models import File

import os


class FileIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=False)
    # content = indexes.CharField(model_attr='docfile')
    title = indexes.CharField(model_attr='name')

    def get_model(self):
        return File

    # def prepare(self, obj):
    #     data = super(FileIndex, self).prepare(obj)
    #     file_obj = obj.docfile.open()

    #     extracted_data = self.get_backend().extract_file_contents(file_obj)
    #     print(extracted_data['contents'])
    #     extracted_data = self.get_backend().extract_file_contents(file_obj)
    #     print(extracted_data['content'])

    #     print(extracted_data)

        # if extracted_data is not None:
        #     for k, v in extracted_data['metadata'].items():
        #         data["attr_%s" % k] = k
        # else:
        #     self.log.warning("Metadata extraction failed for %s", obj)

        # for k, v in obj.attributes.items():
        #     data["attr_%s" % k] = v
        # print(data)
        # return data
