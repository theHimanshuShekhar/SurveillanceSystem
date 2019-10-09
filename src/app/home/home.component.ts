import { Component, OnInit, ChangeDetectorRef, NgZone } from '@angular/core';
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

  constructor(private electron: ElectronService, private change: ChangeDetectorRef, private zone: NgZone) { }

  ngOnInit() {
    console.clear();

    this.selected = this.tabs[1];

    this.electron.remote.getCurrentWindow().setTitle(this.electron.remote.getCurrentWindow().getTitle() + ' - Home');
    // this.electron.remote.getCurrentWindow().webContents.openDevTools();

    this.folders = new Array();
    this.getFolders();
  }

  getFolders() {
    this.change.detectChanges();
    const path = join(this.appPath, './results');
    // this.fs.readdir(path, (err, files) => {
    //   files.forEach(file => {
    //     this.zone.run(() => {
    //       this.folders.push(file);
    //       console.log(this.folders);
    //     });
    //   });
    // });

    const folders = this.fs.readdirSync(path);
    this.folders = folders.sort().reverse();
  }

  select(tab) {
    this.selected = tab;
  }


}
