import { Component, OnInit } from '@angular/core';
import { ElectronService } from '../core/services';

const { join } = require('path');

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {

  appPath = this.electron.remote.app.getAppPath();
  fs = this.electron.fs;

  selected;

  folders;

  tabs = ['Live View', 'Recordings', 'Configuration'];

  constructor(private electron: ElectronService) { }

  ngOnInit() {
    console.clear();

    this.selected = this.tabs[1];

    this.electron.remote.getCurrentWindow().setTitle(this.electron.remote.getCurrentWindow().getTitle() + ' - Home');
    this.electron.remote.getCurrentWindow().setMenuBarVisibility(false);
    this.electron.remote.getCurrentWindow().webContents.closeDevTools();
    this.folders = new Array();
    // this.getFolders();
    console.log(this.folders);
  }

  getFolders() {
    this.fs.readdirSync(join(this.appPath, './results')).forEach(file => {
      console.log(this.fs.statSync(file));
      // console.log(stats);
    });
  }

  async getFolderStat(file) {
    let filename;
    this.fs.statSync(file);

    return file;
  }

  select(tab) {
    this.selected = tab;
  }


}
