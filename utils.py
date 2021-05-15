class CaseMixin:
    """Contains method used for exporting Models to PascalCase expected in API responses."""
    def export(self):
        exported_object = {}
        for attr, val in self.__dict__.items():
            if not attr.startswith('_'):
                exported_object[self.to_pascal(attr)] = val
        return exported_object

    @staticmethod
    def to_pascal(text):
        """Return text converted from snake_case to PascalCase with special_texts conversion."""
        special_texts = {
            'Id': 'ID',
            'Homepage': 'HomePage'
        }

        output_text = ''.join(word.capitalize() for word in text.split('_'))
        for old, new in special_texts.items():
            output_text = output_text.replace(old, new)
        return output_text
