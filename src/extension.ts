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

    // Create and show a new WebView panel in a split on the right
    const panel = vscode.window.createWebviewPanel(
      'csvFormatterForm',            // Identifies the type of the webview.
      'CSV Formatter Parameters',    // Title of the panel displayed to the user
      vscode.ViewColumn.Beside,        // Open the webview beside the current editor
      { enableScripts: true }          // Enable scripts in the webview
    );

    // Set the HTML content for the WebView panel
    panel.webview.html = getWebviewContent();

    // Listen for messages from the WebView
    panel.webview.onDidReceiveMessage(message => {
      // Build the argument array for the Python script
      const pythonScriptPath = path.join(context.extensionPath, 'resources', 'csvformatter.py');
      let args = [pythonScriptPath, filePath];

      if (message.size && message.size.trim() !== '') {
        args.push('-s', message.size.trim());
      }
      if (message.columns && message.columns.trim() !== '') {
        args.push('-c', message.columns.trim());
      }
      if (message.range && message.range.trim() !== '') {
        args.push('-r', message.range.trim());
      }
      if (message.filter && message.filter.trim() !== '') {
        args.push('-f', message.filter.trim());
      }
      if (message.execute && message.execute.trim() !== '') {
        // Do not wrap the command in additional quotes.
        const execParam = message.execute.trim();
        args.push('-x', execParam);
      }      
      if (message.query) { // -q now stands for Query
        args.push('-q');
      }
      if (message.output && message.output.trim() !== '') {
        args.push('-o', message.output.trim());
      }

      console.log('Spawning Python process with args:', args);

      // Spawn the Python process using python3
      const pythonProcess = spawn('python3', args);

      let outputData = '';
      pythonProcess.stdout.on('data', (data) => {
        outputData += data.toString();
        console.log(`stdout: ${data}`);
      });

      pythonProcess.stderr.on('data', (data) => {
        console.error(`stderr: ${data}`);
      });

      pythonProcess.on('close', (code) => {
        vscode.window.showInformationMessage(`Python script exited with code ${code}`);
        if (code === 0) {
          vscode.workspace.openTextDocument({ content: outputData, language: 'csv' })
            .then(doc => vscode.window.showTextDocument(doc, editor.viewColumn));
        } else {
          vscode.window.showErrorMessage(`Python script exited with code ${code}`);
        }
      });

      // Remove panel.dispose() to keep the window open.
      // panel.dispose();
    });
  });

  context.subscriptions.push(disposable);
}

export function deactivate() {}

// Helper function to return the HTML content for the WebView panel
function getWebviewContent() {
  return `
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <title>CSV Formatter Parameters</title>
      <style>
        body {
          font-family: sans-serif;
          padding: 10px;
        }
        .form-group {
          display: flex;
          align-items: center;
          margin-bottom: 10px;
        }
        .form-group label {
          width: 150px;
          margin-right: 10px;
        }
        .form-group input[type="text"] {
          flex: 1;
          padding: 4px;
        }
        .form-group input[type="checkbox"] {
          margin-left: 0;
        }
        button {
          padding: 6px 12px;
          font-size: 14px;
        }
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
        <div class="form-group">
          <label for="filter">Filter (-f):</label>
          <input type="text" id="filter" name="filter" placeholder="e.g., 3-Integer-float">
        </div>
        <div class="form-group">
          <label for="execute">Execute (-x):</label>
          <input
            type="text"
            id="execute"
            name="execute"
            placeholder="1-&quot;awk -F. '{print $5}'&quot;"
            style="width: 400px; padding: 5px;"
          >          
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
        document.getElementById('csvForm').addEventListener('submit', (event) => {
          event.preventDefault();
          const formData = {
            size: document.getElementById('size').value,
            columns: document.getElementById('columns').value,
            range: document.getElementById('range').value,
            filter: document.getElementById('filter').value,
            execute: document.getElementById('execute').value,
            query: document.getElementById('query').checked,
            output: document.getElementById('output').value
          };
          vscode.postMessage(formData);
        });
      </script>
    </body>
    </html>
  `;
}