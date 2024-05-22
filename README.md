# Proyecto Producto de Datos
# SmartBakery

![](imgs/SmartBakery.jpg)
         
# (MCD ITAM Primavera 2024)

## Autores 📚

| Nombre                     |  CU    | Correo Electrónico | Usuario Github |
|----------------------------|--------|--------------------|----------------|
| Blanca E. García Manjarrez | 118886 | bgarci11@itam.mx   |    BGARCIAMA   |
| Iván García Alba           | 214549 | rgarc199@itam.mx   |    GARCIA889   |
| Valeria Durán Rubio        | 124273 | vduranru@itam.mx   |    VDR90       |
| Yuneri Pérez Arellano      | 199813 | yperezar@itam.mx   |    YunPerez    |



## Contexto  🧠
![](imgs/logo.png)
 
En el competitivo mercado de la panadería, la gestión eficiente del inventario es crucial para maximizar las ganancias y garantizar la satisfacción del cliente. Muchas panaderías enfrentan desafíos significativos, como la predicción inexacta de la demanda, el desperdicio de productos y la falta de disponibilidad de artículos populares.
 
**SmartBakery** nace como una solución innovadora para abordar estos problemas. Al integrar técnicas avanzadas de ciencia de datos, analítica de gran escala y cómputo distribuido, SmartBakery proporciona a las panaderías una herramienta poderosa para optimizar su inventario. Esta optimización se traduce en una reducción de desperdicios, una mejor satisfacción del cliente al asegurar la disponibilidad de productos y, en última instancia, un aumento en las ganancias.
 
SmartBakery no solo predice la demanda de productos, sino que también ofrece visualizaciones atractivas de las ventas reales en periodos de tiempo, inventario en tiempo real, precios y ganancias por cada producto y rankings de los productos más vendidos. Estas herramientas permiten identificar patrones estacionales, eventos locales y condiciones meteorológicas que afectan las trasacciones diarias. De esta manera, las panaderías pueden tomar decisiones informadas y estratégicas, mejorando su eficiencia operativa y fortaleciendo su posición en el mercado.

## Objetivo 🎯
El objetivo de SmartBakery es construir un producto de datos que optimice el inventario de una panadería, mejorando así las ganancias y la satisfacción del cliente. Este producto sigue la metodología del working backwards para presentar una oferta de valor clara y utiliza los componentes del CRISP-DM y el Well Architected Machine Learning Lens.

## Contenido

* [Working Backwards en PDF](working_backwards/00_Working backwards_SmartBakery.pdf)
Los documentos que conforman el working backwards, donde se detalla el proceso y la oferta de valor de SmartBakery, se encuestran en esta sección:

  - **Press Release**
    Aquí puedes leer el comunicado de prensa que describe la propuesta de valor y los beneficios de SmartBakery.
    [Leer Press Release](working_backwards/01_PressRelease_SmartBakery.pdf)

  - **Cinco preguntas alrededor del cliente**
    Respondemos a las cinco preguntas críticas para entender las necesidades y expectativas de nuestros clientes.
    [Leer Documento](working_backwards/02_5Quest_SmartBakery.pdf)

  - **Boceto de la solución**
    El boceto muestra la solución final de SmartBakery, detallando las iteraciones realizadas para llegar al producto final.
    [Ver Boceto](imgs/boceto_SmartBakery.png)

  - **FAQ**
    Respondemos las preguntas más frecuentes de nuestros clientes.
    [Consultarlo](working_backwards/03_FAQ_SmartBakery.pdf)

* **Arquitectura de la solución**
    El siguiente diagrama muestra las conexiones de las interacciones entre los servicios utilizados por la plataforma de SmartBakery.
    ![Ver Diagrama](imgs/SmartBakery.png)

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

  2. **Configuración**: Configura las credenciales de acceso a la base de datos y las APIs necesarias.
  3. **Ejecución**:
    - Correr los scripts en el siguiente orden:
      1. [prep.py](prep.py) 
      2. [aws_s3.py](aws_s3.py) (AWS S3)
      3. [data_prep_bakery.py](data_prep_bakery.py) (AWS Sagemaker)
      4. [bakery_reg_endpoint.ipynb](bakery_reg_endpoint.ipynb)


### Qué tipo de analítica utilizaron
- **Modelos de predicción**: Regresión lineal, árboles de decisión
- **Analítica descriptiva**: Análisis de series de tiempo, visualización de datos históricos
- **Simulaciones**: Análisis de escenarios para distintas estrategias de inventario
 
### Inputs-Outputs
- **Inputs**: Datos históricos de ventas, niveles de inventario, datos meteorológicos, eventos locales
- **Outputs**: Predicciones de demanda, recomendaciones de inventario, alertas de stock
 
### Cómo se utilizan los outputs
Las predicciones y recomendaciones generadas por SmartBakery se utilizan para tomar decisiones informadas sobre el reabastecimiento y gestión de inventario, reduciendo costos y mejorando la disponibilidad de productos.
 
### Costos estimados a un año
El paquete más contratado tiene un costo estimado para implementar y mantener SmartBakery durante un año de:
- **Infraestructura en la nube**: $50,000 MXN
- **Licencias de software**: $14,000 MXN
- **Mantenimiento y soporte**: $35,000 MXN
- **Total**: $99,000 MXN

Contamos con 4 paquetes de contratación mensual o anual que pueden adaptarse a las necesidades de tu panadería. ![Consultar inversión](imgs/Costos_SmartBakery.png) 

## DEMO
https://us-east-1.quicksight.aws.amazon.com/sn/accounts/058264510014/dashboards/dec2155e-6ee5-4c3d-aa87-ac4e4651de09?directory_alias=yunperez

![](imgs/Vista_Previa_SB.png)


## Estructura del repositorio  📂
```
.
├── EDA
│   └── EDA_Bakery.ipynb
├── README.md
├── aws_s3.py
├── bakery_reg_endpoint.ipynb
├── config.yaml
├── data
│   ├── prep
│   │   └── data_bakery_prep.csv
│   └── raw
│       ├── Bakery_Sales.csv
│       └── TempTot.csv
├── environment.yml
├── imgs
│   ├── Costos_SmartBakery.png
│   ├── SmartBakery.jpg
│   ├── SmartBakery.png
│   ├── Vista_Previa_SB.png
│   ├── boceto_SmartBakery.png
│   └── logo.png
├── logs
├── prep_previo.py
├── prep_split_data.py
├── smartbakerypred.json
├── src
│   ├── __pycache__
│   │   └── scripts_prep.cpython-311.pyc
│   └── scripts_prep.py
└── working_backwards
    ├── 00_WorkingBackwards_SmartBakery.pdf
    ├── 01_PressRelease_SmartBakery.pdf
    ├── 02_5Quest_SmartBakery.pdf
    └── 03_FAQ_SmartBakery.pdf
```
