import { Component, OnInit, Input } from '@angular/core';

@Component({
  selector: 'app-recordings',
  templateUrl: './recordings.component.html',
  styleUrls: ['./recordings.component.scss']
})
export class RecordingsComponent implements OnInit {
  @Input() folders;

  constructor() { }

  ngOnInit() {
    console.log(this.folders);
  }

}
