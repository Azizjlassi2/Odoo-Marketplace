"""

 module pour utiliser le type float dans l'url

copier : register_converter(converts.FloatUrlParameterConverter, 'float')


"""
class FloatUrlParameterConverter:
    regex = '[0-9]+\.?[0-9]+'

    def to_python(self, value):
        return float(value)

    def to_url(self, value):
        return str(value)

# copier : register_converter(converts.FloatUrlParameterConverter, 'float')  : dans le document attendu !
