import * as vscode from 'vscode';
import { spawn } from 'child_process';
import * as path from 'path';

export function activate(context: vscode.ExtensionContext) {
  let disposable = vscode.commands.registerCommand('csvformatter.format', async () => {
    const editor = vscode.window.activeTextEditor;
    if (!editor) {
      vscode.window.showErrorMessage('No active editor found.');
      return;
    }
    const document = editor.document;
    const filePath = document.fileName;
    if (path.extname(filePath).toLowerCase() !== '.csv') {
      vscode.window.showErrorMessage('The active file is not a CSV file.');
      return;
    }

    const panel = vscode.window.createWebviewPanel(
      'csvFormatterForm',
      'CSV Formatter Parameters',
      vscode.ViewColumn.Beside,
      { enableScripts: true }
    );

    panel.webview.html = getWebviewContent();

    panel.webview.onDidReceiveMessage(message => {
      const pythonScriptPath = path.join(context.extensionPath, 'resources', 'csvformatter.py');
      let args: string[] = [pythonScriptPath, filePath];

      if (message.size) {
        args.push('-s', message.size.trim());
      }
      if (message.columns) {
        args.push('-c', message.columns.trim());
      }
      if (message.range) {
        args.push('-r', message.range.trim());
      }
      // handle multiple filters
      if (message.filter && Array.isArray(message.filter)) {
        for (const f of message.filter) {
          if (f.trim() !== '') {
            args.push('-f', f.trim());
          }
        }
      }

      if (message.match && message.match.trim() !== '') {
        args.push('-m', message.match.trim());
      }
      if (message.execute && message.execute.trim() !== '') {
        args.push('-x', message.execute.trim());
      }
      if (message.query) {
        args.push('-q');
      }
      if (message.output) {
        args.push('-o', message.output.trim());
      }

      console.log('Spawning Python process with args:', args);
      const pythonProcess = spawn('python3', args);

      let outputData = '';
      pythonProcess.stdout.on('data', d => {
        outputData += d.toString();
      });
      pythonProcess.stderr.on('data', d => {
        console.error(`stderr: ${d}`);
      });
      pythonProcess.on('close', code => {
        vscode.window.showInformationMessage(`Python exited with ${code}`);
        if (code === 0) {
          vscode.workspace.openTextDocument({ content: outputData, language: 'csv' })
            .then(doc => vscode.window.showTextDocument(doc, editor.viewColumn));
        } else {
          vscode.window.showErrorMessage(`Python exited with ${code}`);
        }
      });
    });
  });

  context.subscriptions.push(disposable);
}

export function deactivate() {}

function getWebviewContent() {
  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>CSV Formatter Parameters</title>
  <style>
    body { font-family: sans-serif; padding: 10px; }
    .form-group { display: flex; align-items: center; margin-bottom: 10px; }
    .form-group label { width: 150px; margin-right: 10px; }
    .form-group input[type="text"] { flex: 1; padding: 4px; }
    .form-group input[type="checkbox"] { margin-left: 0; }
    button { padding: 6px 12px; font-size: 14px; }
    #add-filter { margin-left: 5px; }
  </style>
</head>
<body>
  <h2>CSV Formatter Parameters</h2>
  <form id="csvForm">
    <div class="form-group">
      <label for="size">Max Size (-s):</label>
      <input type="text" id="size" name="size" placeholder="default:20, all for fullsize">
    </div>
    <div class="form-group">
      <label for="columns">Columns (-c):</label>
      <input type="text" id="columns" name="columns" placeholder="e.g., 2">
    </div>
    <div class="form-group">
      <label for="range">Range (-r):</label>
      <input type="text" id="range" name="range" placeholder="e.g., 1-3-4">
    </div>
    <!-- filter container -->
    <div id="filter-container">
      <div class="form-group filter-group">
        <label>Filter (-f):</label>
        <input type="text" name="filter" placeholder="e.g., 3-Integer-float or 3-regex:^A.*$" style="flex:1;padding:4px;">
        <button type="button" id="add-filter">+</button>
      </div>
    </div>
    <div class="form-group">
      <label for="match">Match (-m):</label>
      <input type="text" id="match" name="match" placeholder="e.g., 10-1-3-4-7">
    </div>
    <div class="form-group">
      <label for="execute">Execute (-x):</label>
      <input type="text" id="execute" name="execute" placeholder="e.g., 1-&quot;awk -F. '{print $5}'&quot;" style="width:400px;padding:4px;">
    </div>
    <div class="form-group">
      <label for="query">Query (-q):</label>
      <input type="checkbox" id="query" name="query">
    </div>
    <div class="form-group">
      <label for="output">Output (-o):</label>
      <input type="text" id="output" name="output" placeholder="output.csv">
    </div>
    <button type="submit">Submit</button>
  </form>

  <script>
    const vscode = acquireVsCodeApi();
    let filterCount = 1;
    document.getElementById('add-filter').addEventListener('click', () => {
      const container = document.getElementById('filter-container');
      const div = document.createElement('div');
      div.className = 'form-group filter-group';
      div.innerHTML = \`
        <label>Filter (-f):</label>
        <input type="text" name="filter" placeholder="e.g., 3-Integer-float or 3-regex:^A.*$" style="flex:1;padding:4px;">
      \`;
      container.appendChild(div);
      filterCount++;
    });

    document.getElementById('csvForm').addEventListener('submit', (e) => {
      e.preventDefault();
      // gather all filter inputs
      const filters = Array.from(document.querySelectorAll('input[name="filter"]'))
                           .map(i => i.value)
                           .filter(v => v.trim() !== '');
      const message = {
        size: document.getElementById('size').value,
        columns: document.getElementById('columns').value,
        range: document.getElementById('range').value,
        filter: filters,
        match: document.getElementById('match').value,
        execute: document.getElementById('execute').value,
        query: document.getElementById('query').checked,
        output: document.getElementById('output').value
      };
      vscode.postMessage(message);
    });
  </script>
</body>
</html>`;
}
