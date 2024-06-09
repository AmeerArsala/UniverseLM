export function copyTextToClipboard(textToCopy: string) {
  if (navigator?.clipboard?.writeText) {
    return navigator.clipboard.writeText(textToCopy).then(() => {
      console.log('Text copied to clipboard');
    }).catch((error) => {
      console.error('Failed to copy text: ', error);
    });
  }
  return Promise.reject('The Clipboard API is not available.');
}

export async function saveTextFile(textContent: string) {
  const blob = new Blob([textContent], { type: 'text/plain;charset=utf-8' });
  const url = URL.createObjectURL(blob);

  const link = document.createElement('a');
  link.href = url;
  link.download = 'filename.txt'; // Customize the filename as needed
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);

  URL.revokeObjectURL(url);
}
