function previewImage(event) {
  const fileInput = event.target;
  const preview = document.getElementsByClassName("preview-img");
  const previewContainer = document.getElementById("image-preview");

  // Display the selected image in the preview container
  const file = fileInput.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = function (e) {
      preview.src = e.target.result;
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
