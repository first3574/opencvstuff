#include "opencv2/highgui/highgui.hpp"
#include "opencv2/imgproc/imgproc.hpp"
#include "opencv2/core/core.hpp"
#include <iostream>

using namespace cv;
using namespace std;

int main(int argc, char* argv[])
{
    VideoCapture cap(0); // open the video camera no. 0

    if (!cap.isOpened())  // if not success, exit program
    {
        cout << "Cannot open the video cam" << endl;
        return -1;
    }

    double dWidth = cap.get(CV_CAP_PROP_FRAME_WIDTH); //get the width of frames of the video
    double dHeight = cap.get(CV_CAP_PROP_FRAME_HEIGHT); //get the height of frames of the video

    cout << "Frame size : " << dWidth << " x " << dHeight << endl;

    //namedWindow("MyVideo",CV_WINDOW_AUTOSIZE); //create a window called "MyVideo"
    //namedWindow("hsv",CV_WINDOW_AUTOSIZE);
    namedWindow("mask",CV_WINDOW_AUTOSIZE);
    namedWindow("output",CV_WINDOW_AUTOSIZE);

    Mat frame;
    Mat hsv;
    Mat mask;
    Mat tracker;
    Mat output;
    vector<vector<Point>> contours;
    vector<Vec4i> hierarchy;

    while (1)
    {

        bool bSuccess = cap.read(frame); // read a new frame from video
        // Color conversion
        cvtColor(frame, hsv, COLOR_BGR2HSV);
        // Mask for objects in our yellow color range
        auto lowerYel = Scalar(20, 120, 120);
        auto upperYel = Scalar(30, 255, 255);
        inRange(hsv, lowerYel, upperYel, mask);
        // Remove small holes/noise
        erode(mask, tracker, getStructuringElement(MORPH_ELLIPSE, Size(10, 10)));
        dilate(tracker, tracker, getStructuringElement(MORPH_ELLIPSE, Size(5, 5)));
        // Calculate contours
        cvtColor(tracker, output, COLOR_GRAY2BGR);
        findContours( tracker, contours, hierarchy, CV_RETR_CCOMP, CV_CHAIN_APPROX_NONE );
        int curContour = 0;
        for(auto contour : contours)
        {
            auto area = contourArea(contour);
            if(area < 1000)
                drawContours(tracker, contours, curContour, Scalar(0,0,0), -1);
            else
                drawContours(output, contours, curContour, Scalar(0,255,0), 3);
            curContour++;
        }

        // Draw a black frame around the image because for whatever reason our black
        // contours drawn above don't reach the edge of the screen
        Size imSiz = tracker.size();
        rectangle(tracker, Point(0,0), Point(imSiz.width, imSiz.height), Scalar(0,0,0), 2);

        // Calculate moments
        Moments calcdMoments = moments(tracker);
        double dM01 = calcdMoments.m01;
        double dM10 = calcdMoments.m10;
        double dArea = calcdMoments.m00;

        if(dArea > 20000) {
            Mat nonzeroPoints;
            findNonZero(tracker, nonzeroPoints);
            RotatedRect minAreaR = minAreaRect(nonzeroPoints);
            Rect brect = minAreaR.boundingRect();
            rectangle(output, brect, Scalar(0,0,255), 2);

            int posx = dM10 / dArea;
            int posy = dM01 / dArea;
            circle(output, Point(posx, posy), 5, Scalar(25, 200, 50), 10);
        }


        if (!bSuccess) //if not success, break loop
        {
            cout << "Cannot read a frame from video stream" << endl;
            break;
        }

        imshow("mask", mask);
        imshow("output", output);

        if (waitKey(30) == 27) //wait for 'esc' key press for 30ms. If 'esc' key is pressed, break loop
        {
            cout << "esc key is pressed by user" << endl;
            break; 
        }
    }
    return 0;

}
