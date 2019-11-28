import { Component, OnInit } from '@angular/core';
import { ResultService } from 'src/app/services/result.service';

@Component({
  selector: 'app-config',
  templateUrl: './config.component.html',
  styleUrls: ['./config.component.scss']
})
export class ConfigComponent implements OnInit {


  labels = [
    'person',
    'bicycle',
    'car',
    'motorbike',
    'aeroplane',
    'bus',
    'train',
    'truck',
    'boat',
    'traffic light',
    'fire hydrant',
    'stop sign',
    'parking meter',
    'bench',
    'bird',
    'cat',
    'dog',
    'horse',
    'sheep',
    'cow',
    'elephant',
    'bear',
    'zebra',
    'giraffe',
    'backpack',
    'umbrella',
    'handbag',
    'tie',
    'suitcase',
    'frisbee',
    'skis',
    'snowboard',
    'sports ball',
    'kite',
    'baseball bat',
    'baseball glove',
    'skateboard',
    'surfboard',
    'tennis racket',
    'bottle',
    'wine glass',
    'cup',
    'fork',
    'knife',
    'spoon',
    'bowl',
    'banana',
    'apple',
    'sandwich',
    'orange',
    'broccoli',
    'carrot',
    'hot dog',
    'pizza',
    'donut',
    'cake',
    'chair',
    'sofa',
    'pottedplant',
    'bed',
    'diningtable',
    'toilet',
    'tvmonitor',
    'laptop',
    'mouse',
    'remote',
    'keyboard',
    'cell phone',
    'microwave',
    'oven',
    'toaster',
    'sink',
    'refrigerator',
    'book',
    'clock',
    'vase',
    'scissors',
    'teddy bear',
    'hair drier',
    'toothbrush',
  ];

  selected = [];

  constructor(private service: ResultService) { }

  config;

  ngOnInit() {
    // Get Config
    this.service.getConfig().subscribe(data => {
      console.log(data);
      this.config = data;
      this.selected = this.config.selected_labels;
    });
  }

  deselect(label) {
    this.labels.push(label);
    this.selected.splice(this.selected.indexOf(label), 1);
    this.labels = this.labels.filter(alabel => this.selected.indexOf(alabel) < 0);
  }

  select(label) {
    this.selected.push(label);
    this.labels.splice(this.labels.indexOf(label), 1);
  }

  save() {
    this.config = { ...this.config, selected_labels: this.selected };
    // Save Config
    if (this.selected.length > 0) {
      this.service.saveConfig(this.config).subscribe(data => {
        console.log('config.json file has been saved.');
      });
    }
  }
}
