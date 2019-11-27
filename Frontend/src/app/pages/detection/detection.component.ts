import { Component, OnInit, OnDestroy } from '@angular/core';
import { ResultService } from 'src/app/services/result.service';

@Component({
  selector: 'app-detection',
  templateUrl: './detection.component.html',
  styleUrls: ['./detection.component.scss']
})
export class DetectionComponent implements OnInit, OnDestroy {

  folders = [];
  resultObs;
  selected;

  selectedVideo;

  constructor(private detectionService: ResultService) { }

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
    this.selectedVideo = path;
    this.detectionService.getVideo(path).subscribe(resp => {
      console.log(resp);
    });
  }

}
