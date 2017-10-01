from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD, LatentDirichletAllocation
import pandas as pd

df = pd.read_csv('features.csv', encoding='latin1')
# if no title for the day for a compagny, either we give it a 0 value, or we dont give it anything
tmp_text = df['title']
df.drop('title', axis=1, inplace=True)

text_vectorizer = TfidfVectorizer(min_df=2, max_features=50000, stop_words='english')
tf_idf = text_vectorizer.fit_transform(tmp_text)

# LSA prob is nuff
lsa = TruncatedSVD(n_components=50, n_iter=50)
lsa_msg = lsa.fit_transform(tf_idf)
# lda = LatentDirichletAllocation(n_components=50, n_jobs=3, learning_method='batch')
# lda_msg = lda.fit_transform(tf_idf)

# df = df.merge(pd.DataFrame(lda_msg), left_index=True, right_index=True)
df = df.merge(pd.DataFrame(lsa_msg), left_index=True, right_index=True)

tmp_text = df['subreddit']
df.drop('subreddit', axis=1, inplace=True)

text_vectorizer = TfidfVectorizer(min_df=2, max_features=50000, stop_words='english')
tf_idf = text_vectorizer.fit_transform(tmp_text)

# LSA prob is nuff
lsa = TruncatedSVD(n_components=50, n_iter=50)
lsa_msg = lsa.fit_transform(tf_idf)

# lda = LatentDirichletAllocation(n_components=50, n_jobs=3, learning_method='batch')
# lda_msg = lda.fit_transform(tf_idf)

# df = df.merge(pd.DataFrame(lda_msg), left_index=True, right_index=True)
df = df.merge(pd.DataFrame(lsa_msg), left_index=True, right_index=True)

df.to_csv('training_dataset.csv', index=False)