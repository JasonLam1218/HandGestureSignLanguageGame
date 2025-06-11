using UnityEngine;
using System.Collections;
using System.Collections.Generic;
using UnityEngine.Networking;
using System;

public class HandGestureDetector : MonoBehaviour
{
    [Header("Webcam Settings")]
    public int webcamWidth = 640;
    public int webcamHeight = 480;
    public int webcamFPS = 30;

    [Header("Gesture Detection Settings")]
    public float detectionConfidence = 0.7f;
    public float trackingConfidence = 0.5f;

    private WebCamTexture webcamTexture;
    private bool isWebcamInitialized = false;
    private Texture2D processedTexture;
    private Renderer webcamRenderer;

    // Event for gesture detection
    public event Action<string> OnGestureDetected;

    private void Start()
    {
        InitializeWebcam();
        processedTexture = new Texture2D(webcamWidth, webcamHeight);
    }

    private void InitializeWebcam()
    {
        WebCamDevice[] devices = WebCamTexture.devices;
        if (devices.Length == 0)
        {
            Debug.LogError("No webcam found!");
            return;
        }

        webcamTexture = new WebCamTexture(devices[0].name, webcamWidth, webcamHeight, webcamFPS);
        webcamRenderer = GetComponent<Renderer>();
        
        if (webcamRenderer != null)
        {
            webcamRenderer.material.mainTexture = webcamTexture;
        }

        webcamTexture.Play();
        isWebcamInitialized = true;
    }

    private void Update()
    {
        if (!isWebcamInitialized || !webcamTexture.isPlaying)
            return;

        // Process webcam frame
        ProcessFrame();
    }

    private void ProcessFrame()
    {
        if (webcamTexture.isPlaying)
        {
            // Get the current frame
            Color32[] colors = webcamTexture.GetPixels32();
            processedTexture.SetPixels32(colors);
            processedTexture.Apply();

            // TODO: Send frame to ML model for processing
            // This will be implemented to communicate with the Python ML model
            // For now, we'll just simulate gesture detection
            SimulateGestureDetection();
        }
    }

    private void SimulateGestureDetection()
    {
        // TODO: Replace with actual ML model integration
        // This is just a placeholder for testing
        string[] gestures = { "A", "B", "C", "D", "E" };
        string randomGesture = gestures[UnityEngine.Random.Range(0, gestures.Length)];
        OnGestureDetected?.Invoke(randomGesture);
    }

    private void OnDestroy()
    {
        if (webcamTexture != null)
        {
            webcamTexture.Stop();
        }
    }

    public void StartDetection()
    {
        if (!isWebcamInitialized)
        {
            InitializeWebcam();
        }
    }

    public void StopDetection()
    {
        if (webcamTexture != null && webcamTexture.isPlaying)
        {
            webcamTexture.Stop();
        }
    }
} 