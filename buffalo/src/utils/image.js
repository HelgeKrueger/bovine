function dataURItoBlob(dataURI, type) {
  var byteString = atob(dataURI.split(",")[1]);

  var ab = new ArrayBuffer(byteString.length);
  var ia = new Uint8Array(ab);
  for (var i = 0; i < byteString.length; i++) {
    ia[i] = byteString.charCodeAt(i);
  }

  var bb = new Blob([ab], { type: type });
  return bb;
}

export { dataURItoBlob };
