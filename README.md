# Proyecto Producto de Datos
# SmartBakery

![](https://github.com/BGARCIAMA/mge_bakery_forecast/blob/main/imgs/SmartBakery.jpg)
         
# (MCD ITAM Primavera 2024)

## Autores 📚

| Nombre                     |  CU    | Correo Electrónico | Usuario Github |
|----------------------------|--------|--------------------|----------------|
| Blanca E. García Manjarrez | 118886 | bgarci11@itam.mx   |    BGARCIAMA   |
| Iván García Alba           | 214549 | rgarc199@itam.mx   |    GARCIA889   |
| Valeria Durán Rubio        | 124273 | vduranru@itam.mx   |    VDR90       |
| Yuneri Pérez Arellano      | 199813 | yperezar@itam.mx   |    YunPerez    |



## Contexto  🧠
![](https://github.com/BGARCIAMA/mge_bakery_forecast/blob/main/imgs/logo.png)
 
En el competitivo mercado de la panadería, la gestión eficiente del inventario es crucial para maximizar las ganancias y garantizar la satisfacción del cliente. Muchas panaderías enfrentan desafíos significativos, como la predicción inexacta de la demanda, el desperdicio de productos y la falta de disponibilidad de artículos populares.
 
**SmartBakery** nace como una solución innovadora para abordar estos problemas. Al integrar técnicas avanzadas de ciencia de datos, analítica de Gran Escala y Computo Distribuido, SmartBakery proporciona a las panaderías una herramienta poderosa para optimizar su inventario. Esta optimización se traduce en una reducción de desperdicios, una mejor satisfacción del cliente al asegurar la disponibilidad de productos y, en última instancia, un aumento en las ganancias.
 
SmartBakery no solo predice la demanda de productos, sino que también ofrece recomendaciones precisas sobre cuándo y cuánto reabastecer, considerando factores como datos históricos de ventas, patrones estacionales, eventos locales y condiciones meteorológicas. Con esta herramienta, las panaderías pueden tomar decisiones informadas y estratégicas, mejorando su eficiencia operativa y fortaleciendo su posición en el mercado.

## Objetivo 🎯
El objetivo de SmartBakery es construir un producto de datos que optimice el inventario de una panadería, mejorando así las ganancias y la satisfacción del cliente. Este producto sigue la metodología del working backwards para presentar una oferta de valor clara y utiliza los componentes del CRISP-DM y el Well Architected Machine Learning Lens.

## Contenido

- [Working Backwards en PDF](working_backwards) Los documentos que conforman el working backwards, donde se detalla el proceso y la oferta de valor de SmartBakery, se encuestran en esta sección.

- [Press Release](working_backwards/01_PressRelease_SmartBakery.pdf) Aquí puedes leer el comunicado de prensa que describe la propuesta de valor y los beneficios de SmartBakery.

- [Cinco preguntas alrededor del cliente](working_backwards/02_5Quest_SmartBakery.pdf) Respondemos a las cinco preguntas críticas para entender las necesidades y expectativas de nuestros clientes.

- [Boceto de la solución](#boceto-de-la-solución) El boceto muestra la solución final de SmartBakery, detallando las iteraciones realizadas para llegar al producto final.

- [FAQ](working_backwards/03_FAQ_SmartBakery.pdf) Respondemos las preguntas más frecuentes de nuestros clientes.

- [Diagrama de la solución](#diagrama-de-la-solución) 


# Base de datos  ✍
* El principal conjunto de datos utilizado en este análisis pertenece a una panadería francesa y proporciona los detalles de las transacciones diarias de los clientes desde el 1.ene.2021 hasta el 30.sep.2022. El conjunto de datos tiene más de 136 mil transacciones con 6 variables: fecha, hora de la orden, número de ticket, nombre del producto vendido, cantidad y precio unitario del producto. [Base de datos de Kaggle](https://www.kaggle.com/datasets/matthieugimbert/french-bakery-daily-sales?resource=download) 
* Adicionalmente, incluimos datos del clima en Loire-Atlantique, Francia, donde se ubica la panadería. Contamos con datos diarios de 5 variables: temperatura, punto de rocío, lluvia, viento y presión a nivel del mar. Sin embargo, solo utlizamos los datos de temperatura en los días en los que contamos con transacciones para la panadería. [Base de datos de clima](https://www.wunderground.com/history/monthly/fr/bouguenais/LFRS/date/2022-12)

## Requerimientos de Software herramientas recomendadas

1. [Cuenta de Github](https://github.com)
2. [VSCodeIDE](https://code.visualstudio.com)
3. [AWS](https://aws.amazon.com)

### Cómo se utiliza la solución
1. **Instalación**:
   - Clona el repositorio
     ```bash
     git clone https://github.com/Garcia889/mge_bakery_forecast.git
     ```
   - Crea el ambiente
     ```bash
     conda env create --file environments.yml
     conda activate SmartBakery
     ```
   - Agrega variables de ambiente de tu cuenta de AWS
     ```bash
     nano ~/.zshrc
     ```

     ```bash
     export AWS_ACCESS_KEY_ID='YOUR_ACCESS_KEY_ID'
     export AWS_SECRET_ACCESS_KEY='YOUR_SECRET_ACCESS_KEY'
     export AWS_REGION='YOUR_AWS_REGION'
     ```
         
     ```bash
     source ~/.bashrc  # o el archivo correspondiente
     ```

3. **Configuración**: Configura las credenciales de acceso a la base de datos y las APIs necesarias.
4. **Ejecución**: Ejecuta el script principal `smartbakery.py` para iniciar el proceso de optimización.
 
- Correr los scripts en el siguiente orden:
  1. [0.WebScrapping.ipynb](0.WebScrapping.ipynb) 
  2. [bash/1.limpieza.sh](bash/1.limpieza.sh)
  3. [bash/2.union.sh](bash/2.union.sh)
  4. [3.Parte_A.ipynb](3.Parte_A.ipynb)
  5. [4.Parquet_basicos.ipynb](4.Parquet_basicos.ipynb)
  6. [5.Parte_B.ipynb](5.Parte_B.ipynb)


### Qué tipo de analítica utilizaron
- **Modelos de predicción**: Regresión lineal, árboles de decisión
- **Analítica descriptiva**: Análisis de series temporales, visualización de datos históricos
- **Simulaciones**: Análisis de escenarios para distintas estrategias de inventario
 
### Inputs-Outputs
- **Inputs**: Datos históricos de ventas, niveles de inventario, datos meteorológicos, eventos locales
- **Outputs**: Predicciones de demanda, recomendaciones de inventario, alertas de stock
 
### Cómo se utilizan los outputs
Las predicciones y recomendaciones generadas por SmartBakery se utilizan para tomar decisiones informadas sobre el reabastecimiento y gestión de inventario, reduciendo costos y mejorando la disponibilidad de productos.
 
### Costos estimados a un año
El costo estimado para implementar y mantener SmartBakery durante un año incluye:
- **Infraestructura en la nube**: $20,000 MXN
- **Licencias de software**: $7,000 MXN
- **Mantenimiento y soporte**: $11,000 MXN
- **Total**: $38,000 MXN
 
## Diagrama de la solución
El siguiente diagrama muestra cada uno de los componentes de SmartBakery y cómo están interrelacionados. ![Ver Diagrama](https://github.com/BGARCIAMA/mge_bakery_forecast/blob/main/imgs/SmartBakery.png)
