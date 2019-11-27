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

  ngOnDestroy() {
  }

}
