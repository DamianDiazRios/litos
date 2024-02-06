class ConfiguracionBase(object):
    'Configuración base'
    SECRET_KEY = 'awk-9RFG*85'
    DEBUG = True
    TESTING = False
    SQLALCHEMY_DATABASE_URI="mysql+pymysql://damian:Damian1982-@localhost:3306/litos?charset=utf8mb4"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ConfiguracionProduccion(ConfiguracionBase):
    'Configuración de producción'
    DEBUG = True

class ConfiguracionDesarrollo(ConfiguracionBase):
    'Configuración de desarrollo'
    DEBUG = True
    TESTING = True
    SECRET_KEY = 'Desarrollo key'