import { Component, OnInit, OnDestroy } from '@angular/core';
import { ResultService } from 'src/app/services/result.service';
import { timeout } from 'q';
import { Router } from '@angular/router';

@Component({
  selector: 'app-detection',
  templateUrl: './detection.component.html',
  styleUrls: ['./detection.component.scss']
})
export class DetectionComponent implements OnInit, OnDestroy {

  folders = [];
  resultObs;
  showPlayer = false;
  selected;

  selectedVideo;

  constructor(private detectionService: ResultService, private router: Router) { }

  ngOnInit() {
    this.resultObs = this.detectionService.getResults()
      .subscribe(data => {
        Object.keys(data).forEach((key, index) => {
          this.folders.push({
            name: key,
            videos: Object.values(data)[index]
          });
        });
        this.resultObs.unsubscribe();
      });
  }

  select(folder) {
    this.selected = folder;
    this.getThumbs();
  }

  ngOnDestroy() {
    this.resultObs.unsubscribe();
  }

  getThumbs() {
    this.detectionService.getThumb('path').subscribe(resp => console.log(resp));
  }

  deselect() {
    this.selected = null;
  }

  selectVideo(path) {
    this.selectedVideo = 'http://localhost:3000/video?path=' + path;
  }
}
