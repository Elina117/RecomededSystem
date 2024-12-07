## Description of the Completed Work

As part of the assignment, I developed a recommendation system for the student social network. This system generates personalized feeds for users, taking into account their individual characteristics, past activity, and the content of the posts.

### 1. Data Collection
The raw data used included tables containing information about users, their profiles, communities, posts, and user activity (such as likes and post views).

### 2. Understanding User Preferences
For each user, the system analyzes their past activity (e.g., posts they liked, communities they visited) and uses this data to generate recommendations. This allows the system to account for the user’s interests and enhance the relevance of the posts in their feed.

### 3. Recommendation Model Development
I built a recommendation system that considers the following parameters:
- **User profile**: Information about the user (such as age, interests, activity) affects which posts are recommended.
- **User activity**: Viewed posts, likes, and community participation are used to calculate preferences.
- **Post content**: Each post also has certain features (such as tags, communities) that are used to match with users' interests.

### 4. Implementation
I implemented a service that dynamically generates a feed for each user, showing posts most likely to appeal to them based on the factors mentioned above. The system updates the feed in real-time to provide current recommendations.

### 5. Technological Implementation
PostgreSQL was used for data storage, where all data about users, posts, and their activity is stored. I applied data extraction, processing, and analysis methods to build an effective recommendation system.

### 6. Personalizing the Feed
The system selects posts that are not random, but specifically targeted to each user's preferences, ensuring high relevance of the recommendations and improving the user experience on the platform.

### Work Process

#### 1. **Analysis of Three Tables**
First, I analyzed three main tables in the database:
- **User table**: Contains information about each user (such as name, age, interests).
- **Post table**: Contains information about posts published in communities, including the text of the post, tags, and other characteristics.
- **User activity table**: Includes data on user actions (such as likes, post views, community participation).

#### 2. **Feature Extraction**
To improve the model, I extracted new features using various methods:
- **TF-IDF**: Used to extract features from post texts and highlight significant words that could be useful for recommendations.
- **One-Hot Encoding (OHE)**: Applied to encode categorical features, such as tags and community categories, so that the model could use them in training.
- **Mean Target Encoding (MTE)**: Used to encode categorical features by their mean target value, helping to improve model accuracy.
- **Label Encoding**: Used to encode categorical features, such as user and post IDs, into numerical form.

#### 3. **Use of Validation, Standardization, and Class Balancing**
- **Validation**: Cross-validation was used to evaluate the model, reducing the risk of overfitting and improving the model’s overall accuracy.
- **Standardization**: Standardization of numerical features was applied to improve model performance, enabling the models to work better with different data scales.
- **Class balancing**: Methods like oversampling and undersampling were used to handle imbalanced data, especially when certain posts received significantly more likes than others.

#### 4. **Model Training**
I used several machine learning models to build the recommendation system:
- **CatBoost**: A gradient boosting model that works well with categorical features was used to predict the likelihood of a user liking a particular post.
- **Random Forest**: A random forest model was used for classification and generating predictions based on various features.
- **Logistic Regression**: Logistic regression was used for binary classification to predict whether a user will like a post.
- **XGBoost**: Another powerful gradient boosting algorithm was applied to optimize model performance.

#### 5. **Model Evaluation with HitRate@5**
To evaluate the performance of the recommendation system, I used the **HitRate@5** metric. This metric measures how often at least one of the five recommended posts is selected by the user (e.g., receives a like). This metric helps assess the accuracy of recommendations in real-world conditions, where it's important not only to recommend the best post but also to offer several posts among which the user will be interested in one or more.

As a result, the best model for this task was **Random Forest**, which achieved **HitRate@5 = 0.521**. This means that in 52.1% of cases, at least one of the five recommended posts will be selected by the user.

### Result
Now, each user of the social network receives a personalized feed consisting of posts most suitable for their interests and past activity. This enhances user engagement and improves the quality of their interaction with the platform.
