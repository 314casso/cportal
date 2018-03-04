import { Component, ViewChild, OnInit, OnDestroy, AfterViewInit } from '@angular/core';
import { Subscription } from 'rxjs/Subscription';

import {MatPaginator, MatSort, MatTableDataSource} from '@angular/material';

import { TrackingService } from '../_services/tracking.service';
import { Track } from '../_models/track';

@Component({
  selector: 'app-tracking',
  templateUrl: './tracking.component.html',
  styleUrls: ['./tracking.component.css']
})
export class TrackingComponent implements OnInit, AfterViewInit, OnDestroy {
  displayedColumns = [
    'container_number',
    'size',
    'type',
    'line',
    'platform_number',
    'foot',
    'length',
    'model',
    'mtu',
    'train',
    'invoice',
    'departurestation',
    'departuredate',
    'destinationstation',
    'totaldistance',
    'estimatedtime',
    'operationstation',
    'daysinroute',
    'remainingdistance',
    'arrivaldate'
  ];

  tracks$: Subscription;

  dataSource = new MatTableDataSource<Track>();
  resultsLength = 0;

  @ViewChild(MatPaginator) paginator: MatPaginator;
  @ViewChild(MatSort) sort: MatSort;

  applyFilter(filterValue: string) {
    filterValue = filterValue.trim();
    filterValue = filterValue.toLowerCase();
    this.dataSource.filter = filterValue;
  }

  constructor(
    private trackingService: TrackingService
  ) { }

  ngOnInit() {
    this.tracks$ = this.trackingService.getTracks().map(data => {
      const tracks: Track[] = [];
      if (data.length > 0) {
        data[0].tracks.forEach(o => {
          const obj: Track = { } as Track;
          obj.container_number = o.container.number;
          obj.size = o.container.size;
          obj.type = o.container.type;
          obj.line = o.container.line;
          obj.platform_number = o.platform.number;
          obj.foot = o.platform.foot;
          obj.length = o.platform.length;
          obj.model = o.platform.model;
          obj.mtu = o.platform.mtu;
          obj.train = o.raildata.train;
          obj.invoice = o.raildata.invoice;
          obj.departurestation = o.raildata.departurestation;
          obj.departuredate = o.raildata.departuredate;
          obj.destinationstation = o.raildata.destinationstation;
          obj.totaldistance = o.raildata.totaldistance;
          obj.estimatedtime = o.raildata.estimatedtime;
          obj.operationstation = o.railtracking.operationstation;
          obj.daysinroute = o.railtracking.daysinroute;
          obj.remainingdistance = o.railtracking.remainingdistance;
          obj.arrivaldate = o.railtracking.arrivaldate;
          tracks.push(obj);
        });
        this.resultsLength = tracks.length;
      }
      return tracks;
    })
    .subscribe(result => {
      this.dataSource.data = result;
    });
  }

  ngAfterViewInit() {
    this.dataSource.paginator = this.paginator;
    this.dataSource.sort = this.sort;
  }

  ngOnDestroy() {
    this.tracks$.unsubscribe();
  }
}
