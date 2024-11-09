function previewImage(event) {
  const fileInput = event.target;
  const preview = document.getElementsByClassName("preview-img");
  const previewContainer = document.getElementById("image-preview");
  console.log(preview);
  // Display the selected image in the preview container
  const file = fileInput.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = function (e) {
      preview[0].src = e.target.result;
      preview[1].src = e.target.result;

      previewContainer.style.display = "block";
    };
    reader.readAsDataURL(file);
  } else {
    preview.src = "";
    previewContainer.style.display = "none";
  }
}

function showSliderVal(event) {
  const rangeVal = document.getElementById("rangeVal");
  rangeVal.innerText = event.target.value;
}

function sidebarHandler() {
  const sideBar = document.getElementById("sidebar");
  const isOpen = sideBar.style.left === "0px"; // Check if the sidebar is open
  if (isOpen) {
    sideBar.style.left = "-100%"; // Close the sidebar
  } else {
    sideBar.style.left = "0px"; // Open the sidebar
  }
}
