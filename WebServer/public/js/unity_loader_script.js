var unityInstance = UnityLoader.instantiate("unity-container", "Build/UnityGame.json", {onProgress: UnityProgress});

function UnityProgress(unityInstance, progress) {
  // You can implement a loading bar or progress indicator here
  if (!unityInstance.Module) {
    return;
  }
  console.log("Loading Unity: " + (progress * 100) + "%");
  // Example: if (progress === 1) { document.getElementById('loading-overlay').style.display = 'none'; }
} 