# cambridge-parser
Fetch Cambridge word data from CSV


## Vocabulary Workflow

### 1. Extract Words from WordUp  
Use the following JavaScript snippet in the browser console to extract vocabulary words from WordUp:

```javascript
const result = [...document.querySelectorAll(".text-grayscale-800.clamp-line-5.break-word.text-center")]
  .map(el => el.textContent.trim())
  .join("\n");

console.log(result);
```

### 2. Prepare CSV Input
Create a CSV file with one word per line, for example:
```csv
adapt
```

### 3. Generate Anki Import File
The final output should follow the Anki note format:
```csv
單字,單字說明,拼音,詞性,翻譯,例句1,例句1(翻譯),例句2,例句2(翻譯)
adapt,"to change, or to change something, to suit different conditions or uses",əˈdæpt,verb,使適應不同情況（或用途）;改動;改造;改裝;改編,Davies is busy adapting Brinkworth's latest novel for television.,大衛斯正忙著把布林克沃斯的最新小說改編成電視劇。,The play had been adapted for (= changed to make it suitable for) children.,這個劇本已被改編成兒童劇。
```
