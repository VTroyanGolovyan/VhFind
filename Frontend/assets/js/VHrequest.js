function VHrequest(requestOptions) {
  return new Promise((resolve, reject) => {
    let xhr = new XMLHttpRequest();
    xhr.open(
       requestOptions.method,
       requestOptions.url,
       true
    ) // async XMLHttpRequest
    xhr.onload = () => {
      if (xhr.status >= 200 && xhr.status < 300) {
          resolve(xhr.responseText);
      } else {
          reject(xhr.statusText);
      }
    }
    xhr.onerror = () => {
      reject(xhr.statusText);
    }
    xhr.send(requestOptions.data)
  });
}
