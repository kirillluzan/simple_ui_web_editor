from typing import List, Optional, Union
from typing_extensions import Annotated
import uuid

from pydantic import BaseModel, Field, validator

from ..config import su_settings

from .elements import Barcode, HorizontalGallery, Voice, Photo, PhotoGallery, \
    Signature, Vision, Cart, ImageSlider, MenuItem, DimensionElement, TextElement, Fab
from .enums import CVDetectorType, LaunchType
from .containers import LinearLayout, Tiles
from .handlers import CommonHandler, Handler, CVHandler
from .recognition_templates import RecognitionTemplate

class BaseConfigModel(BaseModel):
    class Config:
        allow_population_by_field_name = True
        use_enum_values = True


class MainMenuModel(BaseConfigModel):
    menu_id: str = Field(default='', alias='MenuId', title='ID')
    menu_item: str = Field(default='', alias='MenuItem', title='Key')
    menu_title: str = Field(default='', alias='MenuTitle', title='Name')
    menu_top: bool = Field(default=False, alias='MenuTop', title='Show in toolbar')

    class Config:
        title = 'MainMenu'


class MediaFileModel(BaseConfigModel):
    media_file_data: str = Field(default='', alias='MediafileData')
    media_file_ext: str = Field(default='', alias='MediafileExt')
    media_file_key: str = Field(default='', alias='MediafileKey')  # media

    class Config:
        title = 'Mediafile'


class SQLQueryModel(BaseConfigModel):
    Query: str

    class Config:
        title = 'SQLQuery'


class PyTimerTaskModel(BaseConfigModel):
    py_timer_task_key: str = Field(default='', alias='PyTimerTaskKey', title='Key')
    py_timer_task_def: str = Field(default='', alias='PyTimerTaskDef', title='Handler name')
    py_timer_task_period: str = Field(default='0', alias='PyTimerTaskPeriod', title='Period', description='Период запуска таймера в миллисекундах')
    py_timer_task_build_in: bool = Field(default=False, alias='PyTimerTaskBuilIn', title='Buil-in handler')

    @validator('py_timer_task_period')
    def check_int_value(cls, v):
        try:
            int(v)
        except Exception:
            raise ValueError('Value must be int')
        return v

    class Config:
        title = 'PyTimerTask'


class StyleTemplate(DimensionElement, TextElement):
    name: str


class PyFilesModel(BaseConfigModel):
    file_path: str = ''
    py_file_key: str = Field(alias='PyFileKey', title='PyFileKey')
    py_file_data: Optional[str] = Field(alias='PyFileData', title='PyFileData')

    class Config:
        title = 'PyFile'


class ConfigurationSettingsModel(BaseConfigModel):
    uid: str = uuid.uuid4().hex
    vendor: Optional[str]
    vendor_url: Optional[str]
    vendor_auth: Optional[str]
    handler_split_mode: Optional[bool]
    handler_code: Optional[str]
    handler_url: Optional[str]
    handler_auth: Optional[str]
    dictionaries: Optional[str]

    class Config:
        title = 'ConfigurationSettings'


Element = Annotated[
    Union[
        LinearLayout,
        Tiles,
        Barcode,
        HorizontalGallery,
        Voice,
        Photo,
        PhotoGallery,
        Signature,
        Vision,
        Cart,
        ImageSlider,
        MenuItem,
        Fab

    ], Field(discriminator='type')
]


class OperationsModel(BaseConfigModel):
    type: str = 'Operation'
    name: str = Field(default=su_settings.locale.get('new_screen'), alias='Name')
    timer: bool = Field(default=False, alias='Timer', title='Screen handler on timer')
    hide_toolbar_screen: bool = Field(default=False, alias='hideToolBarScreen', title='Hide top bar')
    hide_bottom_bar_screen: bool = Field(default=False, alias='hideBottomBarScreen', title='Hide button bar')
    no_scroll: bool = Field(default=False, alias='noScroll', title='Disable scrolling for Root Layout')
    handle_key_up: bool = Field(default=False, alias='handleKeyUp', title='Attach a keyboard handler')
    no_confirmation: Optional[bool] = Field(default=False, alias='noConfirmation', title='Close without confirmation')


    elements: List[Element] = Field(default=[], alias='Elements')
    handlers: Optional[List[Handler]] = Field(default=[], alias='Handlers')


    class Config:
        title = 'Operation'


class CVFrames(BaseConfigModel):
    name: str = Field(alias='Name')
    type: str = Field(default='CVFrame')
    cv_online: bool = Field(default=False, alias='CVOnline')
    cv_detector: CVDetectorType = Field(default='', alias='CVDetector')
    cv_resolution: str = Field(alias='CVResolution')  # HD1080
    cv_mode: str = Field(default='', alias='CVMode')  # list_only
    cv_action_buttons: Optional[str] = Field(alias='CVActionButtons')
    cv_recognition_settings: Optional[str] = Field(alias='CVRecognitionSettings')
    recognition_template: Optional[str] = Field(alias='RecognitionTemplate')
    cv_mask: Optional[str] = Field(alias='CVMask')
    cv_action: Optional[str] = Field(alias='CVAction')  # Title
    cv_info: Optional[str] = Field(alias='CVInfo')
    cv_camera_device: Optional[str] = Field(alias='CVCameraDevice')  # "Back"/Front,
    cv_detector_mode: Optional[str] = Field(alias='CVDetectorMode')  # "train"/predict,
    handlers: Optional[List[CVHandler]] = Field(alias='Handlers')

    class Config:
        title = 'CVFrame'


class CVOperationModel(BaseConfigModel):
    name: str = Field(alias='CVOperationName')
    type: str = 'CVOperation'
    hidden: Optional[bool]
    cv_frames: List[CVFrames] = Field(default=[], alias='CVFrames')

    class Config:
        title = 'CVOperation'


class ProcessesModel(BaseConfigModel):
    type: str = 'Process'
    process_name: str = Field(default=su_settings.locale.get('new_process'), alias='ProcessName', title='Process name')
    plan_fact_header: Optional[str] = Field(defaul='', alias='PlanFactHeader')
    define_on_back_pressed: Optional[bool] = Field(default=False,
        alias='DefineOnBackPressed', title='Override back button (ON_BACK_PRESSED input event)')

    hidden: Optional[bool] = Field(default=False, title='Do not display in Menu')

    login_screen: Optional[bool] = Field(default=False, title='Run at startup')

    sc: Optional[bool] = Field(default=False, alias='SC', title='Independent process')

    operations: List[OperationsModel] = Field(alias='Operations')

    class Config:
        title = 'Process'

'''
IntentScannerMessage – имя сообщения сканера
IntentScannerVariable – имя переменной сообщения сканера
IntentScannerLength – имя переменной, в которой храниться длина штрихкода, если он предаётся в виде байт-массива а не строки
IntentScanner – режим работы сканера через интент
CategoryDefault – фильтр по категориям сообщений для сканера штрихкодов
ExchangeFolder – папка обмена. Выбирает папку обмена, при необходимости создает (создание папки работает в Android до 11 версии)
RawConfigurationServiceON – произвольная авторизация
GitFormat – формат для хранения конфигураций на github.com
RawConfigurationURL – URL при варианте произвольной авторизации
RawConfigurationServiceAuth – строка авторизации, заданная вручную для произвольной авторизации
GitCommitsURL – URL коммитов с GitHub
GitStoreURL – URL репозитория на GitHub для использования в качестве магазина
OnlineSplitMode – «разделенный режим» конфигурации и обработчиков
onlineURLListener – URL обработчиков для разделенного режима
onlineURL – URL конфигурации для любого режима
onlineUser – пользователь конфигурации для любого режима
onlineUserListener – пользователь обработчиков для разделенного режима
onlineCode – код справочника Мобильные клиенты
onlinePass – пароль пользователя конфигурации для любого режима
onlinePassListener – пароль пользователя обработчиков
backendURL – URL PostgREST – устарело. Для соединения с Postgre
backendUser – пользователь Postrgre
oDataURL – URL OData
Service_URL – URL сервиса технической информации (подписка на изменение настроек)
offSettings – запрет на настройки
offChat – отключение чата
offToDo – отключение списка дел
offlineMode – принудительный оффлайн режим
beep – сигнал при каждом сканировании
torch – подсветка при сканировании камерой
dialogOnBackPressed – задавать вопрос при закрытии основной программы
gps – получение координат GPS в Переменные перманентно
timer – интервал таймера
connection_limit – максимальное время попытки соединения для онлайн обработчиков, 0 – неограничено
hardwarescan – отключение кнопки сканирование камерой для экранов со штрих-кодом (для аппаратного сканера)
conf_id – ID конфигурации для запросов вида /get_configuration?confid=…
configuration - загрузка текста конфигурации. Можно передать в настройках конфигурацию (через файл), она будет сразу же загружена'''


class QRCodeConfig(BaseModel):
    raw_url: str = Field(alias='RawConfigurationURL')
    raw_service_auth: str = Field(default='', alias='RawConfigurationServiceAuth')
    raw_service_on: bool = Field(default=True, alias='RawConfigurationServiceON')
    online_split_mode: bool = Field(default=True, alias='OnlineSplitMode')
    online_url_listener: str = Field(default='', alias='onlineURLListener')
    online_user_listener: str = Field(default='', alias='onlineUserListener')



class ClientConfigurationModel(BaseConfigModel):
    name: str = Field(
        default=su_settings.locale.get('new_configuration'),
        alias='ConfigurationName')

    description: Optional[str] = Field(default='', alias='ConfigurationDescription')

    version: str = Field(default='0.0.1', alias='ConfigurationVersion')

    processes: List[Union[ProcessesModel, CVOperationModel]] = Field(
        default=[ProcessesModel(Operations=[OperationsModel()])],
        alias='Processes')

    settings: ConfigurationSettingsModel = Field(
        default=ConfigurationSettingsModel(),
        alias='ConfigurationSettings')

    tags: str = Field(default='', alias='ConfigurationTags')
    broadcast_intent: Optional[str] = Field(alias='BroadcastIntent')
    broadcast_variable: Optional[str] = Field(alias='BroadcastVariable')
    face_recognition_url: Optional[str] = Field(alias='FaceRecognitionURL')
    foreground_service: Optional[bool] = Field(alias='ForegroundService')
    stop_foreground_service_on_exit: Optional[bool] = Field(alias='StopForegroundServiceOnExit')
    on_keyboard_main: Optional[bool] = Field(alias='OnKeyboardMain')
    run_python: Optional[bool] = Field(default=True, alias='RunPython')
    launch: Optional[LaunchType] = Field(alias='Launch', title='Menu type')  # Tiles
    launch_process: Optional[str] = Field(alias='LaunchProcess')  # process
    launch_var: Optional[str] = Field(alias='LaunchVar')  # field
    main_menu: Optional[List[MainMenuModel]] = Field(default=[], alias='MainMenu')
    menu_web_template: Optional[str] = Field(alias='MenuWebTemplate')
    media_file: Optional[List[MediaFileModel]] = Field(default=[], alias='Mediafile')
    offline_on_create: Optional[List[SQLQueryModel]] = Field(alias='OfflineOnCreate')
    py_handlers: Optional[str] = Field(alias='PyHandlers')
    py_handlers_path: Optional[str] = Field(default='', alias='pyHandlersPath')
    py_timer_task: Optional[List[PyTimerTaskModel]] = Field(default=[], alias='PyTimerTask')
    py_files: Optional[List[PyFilesModel]] = Field(default=[], alias='PyFiles')
    style_templates: Optional[List[StyleTemplate]] = Field(default=[], alias='StyleTemplates')
    arch2: bool = True
    common_handlers: Optional[List[CommonHandler]] = Field(default=[], alias='CommonHandlers')
    recognition_templates: Optional[List[RecognitionTemplate]] = Field(alias='RecognitionTemplates')

    class Config:
        title = 'ClientConfiguration'


class RootConfigModel(BaseConfigModel):
    client_configuration: ClientConfigurationModel = Field(default=ClientConfigurationModel(),
                                                           alias='ClientConfiguration')
