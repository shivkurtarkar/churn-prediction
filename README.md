# Predicting Customer Churn for Music streaming service

## Index
- Problem Description
- Dataset Description
- Data Extraction and Challenges
- Dataset Setup
- Dataset Directory
- Project Directory
- Instructions


## Problem Description

In the highly competitive subscription-based music streaming industry, customer churn poses a significant challenge. **Churn** refers to customers not renewing or actively canceling their subscriptions. This issue is critical because retaining existing customers is often more cost-effective than acquiring new ones, and it directly impacts a company’s revenue and growth potential.

The primary objective of this project is to predict whether a user will churn after their subscription expires. Accurately forecasting churn allows streaming platforms to implement proactive retention strategies such as personalized offers, improved customer support, or tailored recommendations. These strategies can help reduce revenue loss and enhance customer lifetime value.

By solving this problem, we aim to assist music streaming services in:
- Identifying customers at risk of churning.
- Gaining insights into user behavior and churn patterns.
- Enabling data-driven decisions to optimize customer retention efforts.

This predictive model will provide actionable insights to empower business teams in reducing churn rates and driving sustainable growth.

## Dataset Description

The dataset used for this project is sourced from the [KKBOX Churn Prediction Challenge on Kaggle](https://www.kaggle.com/competitions/kkbox-churn-prediction-challenge/data). KKBOX is a subscription-based music streaming service where users can choose between manual and auto-renew options and cancel subscriptions at any time.

**Key aspects of the dataset:**

- **Target Variable:**
  - `is_churn`: Indicates whether a user did not renew their subscription within 30 days of expiration. (`is_churn = 1` means churn; `is_churn = 0` means renewal).

- **Dataset Timeframes:**
  - The training data includes users whose subscriptions expired in February 2017, with churn predictions focused on March 2017.
  - The test data includes users whose subscriptions expired in March 2017, with predictions focused on April 2017.

- **Churn Definition Nuances:**
  - Churn is defined as the absence of a valid new subscription within 30 days of the current membership's expiration.
  - Active cancellations do not necessarily imply churn; users may cancel subscriptions to switch plans or for other reasons but still renew later.

**Key Files in the Dataset:**

1. **train.csv / train_v2.csv**
   - User IDs and churn status (target variable).
2. **sample_submission_zero.csv / sample_submission_v2.csv**
   - Test set containing user IDs and expected churn predictions.
3. **transactions.csv / transactions_v2.csv**
   - User transaction details, including payment methods, plan prices, and cancellation statuses.
4. **user_logs.csv / user_logs_v2.csv**
   - Daily listening behaviors, including the number of songs played, unique songs, and total playtime.
5. **members.csv / members_v3.csv**
   - User demographic information such as age, gender, and registration details.

The dataset also includes a churn labeling script (`WSDMChurnLabeller.scala`) to generate churn labels for the user data. This script facilitates the creation of custom training datasets by applying consistent churn definitions.

## Data Extraction and Challenges

One of the key challenges in this project is understanding the intricacies of KKBOX’s subscription model, such as:
- Handling cases where users change their subscription plans.
- Identifying active cancellations versus churn.
- Managing outliers in user demographics (e.g., unrealistic age values).

The dataset provides rich transactional and behavioral data, allowing us to explore diverse features and model customer behavior effectively.

## Dataset Setup

The dataset can be downloaded using the following Kaggle command:

```bash
kaggle competitions download -c kkbox-churn-prediction-challenge
```

## Dataset Directory
Download and organize the dataset as follows:
```
/data  
    members_v3.csv  
    sample_submission_v2.csv  
    sample_submission_zero.csv  
    train.csv  
    train_v2.csv  
    transactions.csv  
    transactions_v2.csv  
    user_logs.csv  
    user_logs_v2.csv  
```

## Project Directory
```
/notebooks  
    /eda  
        eda_dask4.ipynb       # Exploratory Data Analysis notebook  
    /modeling  
        train_v3.ipynb        # Model training notebook  
        train_v4.ipynb        # Notebook with separate training and test data across months  
        train_v5_1.py         # Feedforward Neural Network model training script  
        train_v5_2.py         # Hyperparameter tuning script  

/services  
    /churn_prediction  
        /api                  # API code for churn prediction  
        /test                 # API unit testing scripts  
    /frontend                 # Streamlit application to consume the API  
```

## Instructions

1. **Prepare the Dataset**  
   - Download the dataset files listed above and place them in the `/data` directory.

2. **Update File Paths**  
   - Check and update the file path variables in the notebooks or scripts as needed to ensure they point to the `/data` directory.

3. **Run EDA Notebooks**  
   - Navigate to the `/notebooks/eda` folder.  
   - Open and run `eda_dask4.ipynb` for Exploratory Data Analysis.

4. **Run Model Training**  
   - Navigate to the `/notebooks/modeling` folder.  
   - Use the following notebooks or scripts for model training:  
     - `train_v3.ipynb` for general model training.  
     - `train_v4.ipynb` for training and testing with separate monthly data.  
     - `train_v5_1.py` for training a Feedforward Neural Network.  
     - `train_v5_2.py` for hyperparameter tuning.

5. **Run API and Frontend**  
   - Navigate to the `/services/churn_prediction` directory:  
     - `/api`: Contains the API code. Run the API server from here.  
     - `/test`: Contains unit testing scripts for the API.  
   - Navigate to `/services/frontend`:  
     - Run the Streamlit application to interact with the API.








## instructions for model dev

1. **Create a Virtual Environment**:
   ```bash
   python -m venv myenv
   ```
   Replace `myenv` with your desired environment name.

2. **Activate the Virtual Environment**:
   - On Windows:
     ```bash
     myenv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source myenv/bin/activate
     ```

3. **Install dependecies**:
   ```bash
   pip install -r notebooks/requirements.txt
   ```

4. **Start Jupyter Notebook**:
   ```bash
   jupyter notebook
   ```


5. **to register kernel for vscode (optional)**
   ```bash
   python -m ipykernel install --user --name=cp_env --display-name "myenv"
   ```
---

### Accessing Jupyter:
- After running the `jupyter notebook` command, a new tab should open in your web browser. If it doesn't, copy the provided URL (including the token) and paste it into your browser.


## Setup & Instructions to Get Data

The following steps outline how to set up the environment and access the data:

1.  **Clone the repository:**

    ```bash
    git clone [invalid URL removed]
    cd banking-churn-prediction
    ```

2.  **Create a virtual environment (recommended):**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Linux/macOS
    venv\Scripts\activate     # On Windows
    ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Data Acquisition:**

    *   If using a publicly available dataset, download it and place it in the `data/` directory. The specific download instructions will be in `notebook.ipynb`.
    *   If using synthetic data, the `notebook.ipynb` will contain the code to generate it and save it to the `data/` directory.

## Project Structure

*   `data/`: Contains the datasets used in the project.
*   `notebook.ipynb`: Jupyter Notebook containing data preparation, EDA, model training, and evaluation.
*   `train.py`: Python script for training the final model.
*   `Dockerfile`: Dockerfile for containerizing the application.
*   `requirements.txt`: List of Python dependencies.
*   `README.md`: This file.

## Model Usage

Instructions on how to run the model for predictions will be provided in the `README.md` within the "Productionizing" and "Deployment" sections.

## Deliverables

*   `README.md`: This file.
*   `notebook.ipynb`: Jupyter Notebook with data preparation, EDA, and model development.
*   `train.py`: Python script for training the final model.
*   `Dockerfile`: Dockerfile for deployment.
*   `requirements.txt`: List of dependencies.

## Further Development

Future work could include:

*   Exploring more advanced machine learning models.
*   Implementing real-time churn prediction.
*   Integrating the model into a production environment.
*   Deploying the service to the cloud.


## TODO

- Problem description
- Data Description
- Data extraction and challenges
- Model development
    - EDA
    - model evaluation
- productionization
    - explaination of architecture
    - running service
    - dashboard
        -   Identifying customers at risk of churning.
        - Gaining insights into user behavior and churn patterns.
        - Enabling data-driven decisions to optimize customer retention efforts.

    - monitoring
- cicd
    - explaination
    - instructions