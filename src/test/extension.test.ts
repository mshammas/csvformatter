import * as assert from 'assert';
import * as vscode from 'vscode';

suite('CSV Formatter Extension Test Suite', () => {
  vscode.window.showInformationMessage('Start all tests for CSV Formatter extension.');

  test('Extension should be present', () => {
    const extension = vscode.extensions.getExtension('mshammas.csvformatter');
    assert.ok(extension, 'CSV Formatter extension is not present');
  });

  test('Extension should activate', async () => {
    const extension = vscode.extensions.getExtension('mshammas.csvformatter');
    if (extension) {
      await extension.activate();
      assert.ok(extension.isActive, 'CSV Formatter extension did not activate');
    } else {
      assert.fail('CSV Formatter extension not found');
    }
  });

  test('Command csvformatter.format should be registered', async () => {
    // Fetch all commands, including extension-provided commands
    const commands = await vscode.commands.getCommands(true);
    const csvCommand = commands.find(cmd => cmd === 'csvformatter.format');
    assert.ok(csvCommand, 'Command csvformatter.format is not registered');
  });
});