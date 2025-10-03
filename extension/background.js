chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    id: "word-store-selection",
    title: 'Send word: "%s"',
    contexts: ["selection"]
  })
})

chrome.contextMenus.onClicked.addListener((info, tab) => {
  if (info.menuItemId === "word-store-selection") {
    const selected = info.selectionText || ""
    fetch('http://127.0.0.1:8000/api/add-word', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ word: selected })
    }).catch(e => console.error(e))
  }
})
