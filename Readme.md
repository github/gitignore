Una colección de .gitignoreplantillas
Esta es la colección de .gitignoreplantillas de archivos de GitHub . Usamos esta lista para completar los .gitignoreselectores de plantillas disponibles en la interfaz de GitHub.com al crear nuevos repositorios y archivos.

Para obtener más información sobre cómo .gitignorefuncionan los archivos y cómo usarlos, los siguientes recursos son un excelente lugar para comenzar:

El capítulo Ignorar archivos del libro Pro Git .
El artículo Ignorar archivos en el sitio de ayuda de GitHub.
La página de manual de gitignore (5) .
Estructura de carpetas
Apoyamos una colección de plantillas, organizadas de esta manera:

la carpeta raíz contiene plantillas de uso común, para ayudar a las personas a comenzar con tecnologías y lenguajes de programación populares. Estos definen un conjunto significativo de reglas para ayudarlo a comenzar y garantizar que no esté ingresando archivos sin importancia en su repositorio.
Globalcontiene plantillas para varios editores, herramientas y sistemas operativos que se pueden utilizar en diferentes situaciones. Se recomienda que los agregue a su plantilla global o fusione estas reglas en las plantillas específicas de su proyecto si desea usarlas de forma permanente.
communitycontiene plantillas especializadas para otros lenguajes, herramientas y proyectos populares, que actualmente no pertenecen a las plantillas convencionales. Estos deben agregarse a las plantillas específicas de su proyecto cuando decida adoptar el marco o la herramienta.
¿Qué hace una buena plantilla?
Una plantilla debe contener un conjunto de reglas para ayudar a que los repositorios de Git funcionen con un lenguaje, marco, herramienta o entorno de programación específico.

Si no es posible seleccionar un pequeño conjunto de reglas útiles para esta situación, entonces la plantilla no es adecuada para esta colección.

Si una plantilla es principalmente una lista de archivos instalados por una versión particular de algún software (por ejemplo, un marco PHP), podría residir en el community directorio. Consulte las plantillas versionadas para obtener más detalles.

Si tiene un pequeño conjunto de reglas o desea admitir una tecnología que no se usa ampliamente y aún cree que esto será útil para otros, lea la sección sobre plantillas especializadas para obtener más detalles.

Incluya detalles al abrir la solicitud de extracción si la plantilla es importante y visible. Es posible que no lo aceptemos de inmediato, pero podemos promoverlo a la raíz en una fecha posterior según el interés.

Por favor, comprenda también que no podemos enumerar todas las herramientas que existieron. Nuestro objetivo es seleccionar una colección de las plantillas más comunes y útiles , no asegurarnos de cubrir todos los proyectos posibles. Si optamos por no incluir su lenguaje, herramienta o proyecto, no es porque no sea genial.

Contribución de pautas
Nos encantaría que nos ayudaras a mejorar este proyecto. Para ayudarnos a mantener esta colección de alta calidad, solicitamos que las contribuciones se adhieran a las siguientes pautas.

Proporcione un enlace a la página de inicio de la aplicación o el proyecto . A menos que sea extremadamente popular, existe la posibilidad de que los mantenedores no conozcan o no utilicen el lenguaje, el marco, el editor, la aplicación o el proyecto al que se aplica el cambio.

Proporcione enlaces a la documentación que respalde el cambio que está realizando. La documentación canónica actual que menciona los archivos que se ignoran es la mejor. Si la documentación no está disponible para respaldar su cambio, haga lo mejor que pueda para explicar para qué sirven los archivos que se ignoran.

Explique por qué está haciendo un cambio . Incluso si parece evidente, por favor tome una oración o dos para decirnos por qué debería ocurrir su cambio o adición. Es especialmente útil articular por qué este cambio se aplica a todos los que trabajan con la tecnología aplicable, en lugar de solo a usted o su equipo.

Considere el alcance de su cambio . Si su cambio es específico para un determinado idioma o marco, asegúrese de que el cambio se realiza en la plantilla para ese idioma o marco, en lugar de en la plantilla para un editor, herramienta o sistema operativo.

Modifique solo una plantilla por solicitud de extracción . Esto ayuda a mantener las solicitudes de extracción y los comentarios centrados en un proyecto o tecnología específicos.

En general, cuanto más pueda hacer para ayudarnos a comprender el cambio que está realizando, es más probable que aceptemos su contribución rápidamente.

Plantillas versionadas
Algunas plantillas pueden cambiar mucho entre versiones, y si desea contribuir a este repositorio, debemos seguir este flujo específico:

la plantilla en la raíz debe ser la versión compatible actual
la plantilla en la raíz no debe tener una versión en el nombre del archivo (es decir, "perenne")
las versiones anteriores de las plantillas deben vivir bajo community/
las versiones anteriores de la plantilla deben incrustar la versión en el nombre del archivo, para facilitar la lectura
Esto ayuda a garantizar que los usuarios obtengan la última versión (porque usarán lo que esté en la raíz), pero ayuda a los mantenedores a admitir versiones anteriores que aún están disponibles.

Plantillas especializadas
Si tiene una plantilla que le gustaría contribuir, pero no es muy común, considere agregarla al communitydirectorio en la carpeta que mejor se adapte a su lugar.

Las reglas de su plantilla especializada deben ser específicas del marco o herramienta, y cualquier plantilla adicional debe mencionarse en un comentario en el encabezado de la plantilla.

Por ejemplo, esta plantilla podría vivir en community/DotNet/InforCRM.gitignore:

# gitignore template for InforCRM (formerly SalesLogix)
# website: https://www.infor.com/product-summary/cx/infor-crm/
#
# Recommended: VisualStudio.gitignore

# Ignore model files that are auto-generated
ModelIndex.xml
ExportedFiles.xml

# Ignore deployment files
[Mm]odel/[Dd]eployment

# Force include portal SupportFiles
!Model/Portal/*/SupportFiles/[Bb]in/
!Model/Portal/PortalTemplates/*/SupportFiles/[Bb]in
Contribuir al flujo de trabajo
Así es como le sugerimos que proponga un cambio en este proyecto:

Bifurca este proyecto a tu cuenta.
Cree una rama para el cambio que desea realizar.
Haz tus cambios en tu bifurcación.
Envíe una solicitud de extracción desde la sucursal de su fork a nuestra mastersucursal.
El uso de la interfaz basada en web para realizar cambios también está bien, y lo ayudará a bifurcar automáticamente el proyecto y le pedirá que envíe una solicitud de extracción también.

Licencia
CC0-1.0 .
