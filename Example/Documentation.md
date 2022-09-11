# Blobber for Python Beginners

To utilise Blobber, the best interface would be running Python on Jupyter Notebook. However, if one does not have previous experiences with Jupyter Notebook or Python, here is a step by step guide to install Jupyter Notebook.

## 1) Installing Anaconda on your computer

Since there is already an official step by step guide on installing Anaconda. I will not re-iterate the installation steps. One can find the official installation guide for [Windows here](https://docs.anaconda.com/anaconda/install/windows/); And for macOS, the installation guide is [here](https://docs.anaconda.com/anaconda/install/mac-os/).

## 2) Opening Jupyter Notebook on your computer

After installing Anaconda, open the Anaconda navigator, you should see something like this, where Jupyter note book is already in the navigator.

![Anaconda Navigator](images/Anaconda%20Navigator.png "Anaconda Navigator")

Now, simply click on the launch button, an instance of Jupyter Notebook should automatically open in your default browswer. You should see your file directory display as it is shown in the picture below.

![Jupyter Directory](images/Jupyter%201.png "Jupyter Directory")

You can now freely navigate to different directories via this file directory interface.

## 3) Opening a Terminal in Jupyter Notebook

It is important that you use the **terminal in Jupyter Notebook**, to do that, click on the `New` tab then click on the `Terminal` tab, as shown in the figure below.

![New Jupyter Terminal](images/Jupyter%202.png "New Jupyter Terminal")

## 4) Installing Blobber in your default Anaconda Python environment

Assuming now you are in your terminal that you opened a moment ago in Jupyter Notebook. You need to firstly activate your default Anaconda Python environment. This can be done via typing the following command in the terminal:

    conda activate

Then, you can install Blobber one one simple command:

    python -m pip install blobber

Now, assuming you have followed the above steps correctly, you should have now have Blobber installed and ready to go!

Following is a screenshot of my terminal after I have ran the above steps.

![Terminal Screenshot](images/Terminal%201.png "Terminal Screenshot")

## 5) Creating a Jupyter Notebook file

Now, you can create a new Jupyter Notebook file in any directories of your preferences by clicking the `New` tab and seltect the `Python 3 (ipykernel)` tab as shwon in the image below.

![New Jupyter Notebook](images/Jupyter%203.png "New Jupyter Notebook")

It should automatically redirect you to the newly created file, and to rename it, you need to click on the default name on the top left corner as shown in the following image.

![Change Jupyter Notebook File Name](images/Jupyter%204.png "Change File name")

If you have gotten to here, you are now officially ready to use Blobber!
