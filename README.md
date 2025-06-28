# Image Semantic segmentation

This repository entails code and resources from a machine learning competition on semantic Image segmentation.
This project is hosted on kaggle and the dataset contains images and their respective masks. Semantic image segmentation provides pixel wise compared to that of object localization in which a bounding box is applied on the detected image. It has various use cases like in self driving cars and biomedics

The goal of this project is to build a model to segment images on the data trained on. 

# Model architecture
The semantic segmentation model is based on the U-Net architecture, widely used for image segmentation tasks. The U-Net model consists of an encoder path that captures the context of the image and a decoder path that performs upsampling and produces the segmentation mask.

![Alt text](https://lmb.informatik.uni-freiburg.de/people/ronneber/u-net/u-net-architecture.png)

Due to computational reason I reduced the model complexity by reducing the filters to 32 (original is 64) therefore resulting in a less accurate prediction. This project just serves as a sneak peek to what the original model can achieve.


If you are interested in the competition or just want to learn more about the project, you can check the resources in this repositiory.

# Dataset
This model was trained on labels being cars and their target being masks. The data can be found here on [kaggle](https://www.kaggle.com/datasets/intelecai/car-segmentation)

# Usage
1. Create a virtual environment in the command line
```python 
python3.9 -m venv Segmentation
```
Activate the env:
For macos:
```python 
source Segmentation/bin/activate
```
For windows:
```python
Segmentation\Scripts\activate
```
2. Clone the repository
```python
git clone https://github.com/Abdulmateen7827/Image_segmentation.git
```
cd into
3. Download the image dataset and save locally. The default path is data/ in this repository.

4. Install the project dependencies:
```python 
pip install -r requirements.txt
```
5. Start the training by :
```python 
python src/components/data_ingestion.py
```
6. For prediction using streamlit:
```python
streamlit run streamlit_app.py



