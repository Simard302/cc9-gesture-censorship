# Introduction
Our goal is to censor gestures. To recognize the landmarks, we used Google’s mediapipe software, which comes with a pre-trained hand recognition model. Our innovations came from gesture recognition. We encoded the landmarks as features by creating a distance matrix between each landmark and every other landmark. These distances were then used in a support vector machine to classify the type of gesture. We found a dataset of 600 images, with 31 unique gestures. We then added to this dataset by curating over 50 images of middle finger gestures. Using this dataset, we can train a model that is good at classifying the middle finger gesture. Next, we blur the hand by using each landmark as a point and mapping a gaussian density around the points. We use the OpenCV blur function to blur the pixels that have density.

The repository also includes a website made with Django for uploading files to censor. It comes with a dockerfile to create a stateless image which can be easily deployed with Google Cloud Run (example commands in application/deploy.sh)

# Web demo
[Code Cloud 9 -- Video Censor](https://video-censor.codecloud9.dev/index)

# Contributors 
- Adam Simard
- Zuhayr Mahmood
- Eric Huang
- Daniel Cho
- Kevin Wang
