<template>
  <div class="page">
    <PageHeader />
    <PageNavigation />
    <div class="page-wrapper">
      <div class="container-xl">
        <!-- Page title -->
        <div class="page-header d-print-none">
          <div class="row align-items-center">
            <div class="col">
              <!-- Page pre-title -->
              <h2 class="page-title">Dashboard</h2>
            </div>
          </div>
        </div>
      </div>
      <div class="page-body">
        <div class="container-xl">
          <div class="row row-cards">
            <div class="col-sm-4 col-lg-4">
              <div class="card">
                <div class="card-body">
                  <div class="d-flex align-items-center">
                    <div class="subheader">Winrate</div>
                  </div>
                  <div class="d-flex align-items-baseline">
                    <div class="h1 mb-0 me-2">49%</div>
                    <div class="me-auto">
                      <span class="text-green d-inline-flex align-items-center lh-1">
                        8%
                        <svg xmlns="http://www.w3.org/2000/svg" class="icon ms-1" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"></path><polyline points="3 17 9 11 13 15 21 7"></polyline><polyline points="14 7 21 7 21 14"></polyline></svg>
                      </span>
                    </div>
                  </div>
                </div>
                <div id="chart-revenue-bg" class="chart-sm" style="min-height: 40px;"><div id="apexchartshwhojcwil" class="apexcharts-canvas apexchartshwhojcwil apexcharts-theme-light" style="width: 414px; height: 40px;"><svg id="SvgjsSvg1001" width="414" height="40" xmlns="http://www.w3.org/2000/svg" version="1.1" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:svgjs="http://svgjs.dev" class="apexcharts-svg" xmlns:data="ApexChartsNS" transform="translate(0, 0)" style="background: transparent;"><g id="SvgjsG1003" class="apexcharts-inner apexcharts-graphical" transform="translate(0, 0)"><defs id="SvgjsDefs1002"><clipPath id="gridRectMaskhwhojcwil"><rect id="SvgjsRect1039" width="420" height="42" x="-3" y="-1" rx="0" ry="0" opacity="1" stroke-width="0" stroke="none" stroke-dasharray="0" fill="#fff"></rect></clipPath><clipPath id="forecastMaskhwhojcwil"></clipPath><clipPath id="nonForecastMaskhwhojcwil"></clipPath><clipPath id="gridRectMarkerMaskhwhojcwil"><rect id="SvgjsRect1040" width="418" height="44" x="-2" y="-2" rx="0" ry="0" opacity="1" stroke-width="0" stroke="none" stroke-dasharray="0" fill="#fff"></rect></clipPath></defs><line id="SvgjsLine1008" x1="0" y1="0" x2="0" y2="40" stroke="#b6b6b6" stroke-dasharray="3" stroke-linecap="butt" class="apexcharts-xcrosshairs" x="0" y="0" width="1" height="40" fill="#b1b9c4" filter="none" fill-opacity="0.9" stroke-width="1"></line><g id="SvgjsG1047" class="apexcharts-xaxis" transform="translate(0, 0)"><g id="SvgjsG1048" class="apexcharts-xaxis-texts-g" transform="translate(0, -4)"></g></g><g id="SvgjsG1058" class="apexcharts-grid"><g id="SvgjsG1059" class="apexcharts-gridlines-horizontal" style="display: none;"><line id="SvgjsLine1061" x1="0" y1="0" x2="414" y2="0" stroke="#e0e0e0" stroke-dasharray="4" stroke-linecap="butt" class="apexcharts-gridline"></line><line id="SvgjsLine1062" x1="0" y1="8" x2="414" y2="8" stroke="#e0e0e0" stroke-dasharray="4" stroke-linecap="butt" class="apexcharts-gridline"></line><line id="SvgjsLine1063" x1="0" y1="16" x2="414" y2="16" stroke="#e0e0e0" stroke-dasharray="4" stroke-linecap="butt" class="apexcharts-gridline"></line><line id="SvgjsLine1064" x1="0" y1="24" x2="414" y2="24" stroke="#e0e0e0" stroke-dasharray="4" stroke-linecap="butt" class="apexcharts-gridline"></line><line id="SvgjsLine1065" x1="0" y1="32" x2="414" y2="32" stroke="#e0e0e0" stroke-dasharray="4" stroke-linecap="butt" class="apexcharts-gridline"></line><line id="SvgjsLine1066" x1="0" y1="40" x2="414" y2="40" stroke="#e0e0e0" stroke-dasharray="4" stroke-linecap="butt" class="apexcharts-gridline"></line></g><g id="SvgjsG1060" class="apexcharts-gridlines-vertical" style="display: none;"></g><line id="SvgjsLine1068" x1="0" y1="40" x2="414" y2="40" stroke="transparent" stroke-dasharray="0" stroke-linecap="butt"></line><line id="SvgjsLine1067" x1="0" y1="1" x2="0" y2="40" stroke="transparent" stroke-dasharray="0" stroke-linecap="butt"></line></g><g id="SvgjsG1041" class="apexcharts-area-series apexcharts-plot-series"><g id="SvgjsG1042" class="apexcharts-series" seriesName="Profits" data:longestSeries="true" rel="1" data:realIndex="0"><path id="SvgjsPath1045" d="M 0 40L 0 25.2C 4.99655172413793 25.2 9.279310344827586 26 14.275862068965516 26C 19.272413793103446 26 23.555172413793102 22.4 28.551724137931032 22.4C 33.54827586206896 22.4 37.83103448275862 28.8 42.82758620689655 28.8C 47.82413793103448 28.8 52.106896551724134 25.6 57.103448275862064 25.6C 62.099999999999994 25.6 66.38275862068966 30.4 71.37931034482759 30.4C 76.37586206896552 30.4 80.65862068965517 14 85.6551724137931 14C 90.65172413793103 14 94.93448275862069 27.6 99.93103448275862 27.6C 104.92758620689655 27.6 109.2103448275862 25.2 114.20689655172413 25.2C 119.20344827586206 25.2 123.48620689655172 24.4 128.48275862068965 24.4C 133.47931034482758 24.4 137.76206896551724 15.2 142.75862068965517 15.2C 147.7551724137931 15.2 152.03793103448277 19.6 157.0344827586207 19.6C 162.03103448275863 19.6 166.31379310344826 26 171.3103448275862 26C 176.30689655172412 26 180.58965517241379 23.6 185.58620689655172 23.6C 190.58275862068965 23.6 194.8655172413793 26 199.86206896551724 26C 204.85862068965517 26 209.14137931034483 29.2 214.13793103448276 29.2C 219.1344827586207 29.2 223.41724137931033 2.799999999999997 228.41379310344826 2.799999999999997C 233.4103448275862 2.799999999999997 237.69310344827585 18.8 242.68965517241378 18.8C 247.6862068965517 18.8 251.96896551724137 15.600000000000001 256.9655172413793 15.600000000000001C 261.96206896551723 15.600000000000001 266.2448275862069 29.2 271.2413793103448 29.2C 276.23793103448276 29.2 280.5206896551724 18.4 285.51724137931035 18.4C 290.5137931034483 18.4 294.79655172413794 22.8 299.7931034482759 22.8C 304.7896551724138 22.8 309.07241379310346 32.4 314.0689655172414 32.4C 319.0655172413793 32.4 323.34827586206893 21.6 328.34482758620686 21.6C 333.3413793103448 21.6 337.62413793103445 24.4 342.6206896551724 24.4C 347.6172413793103 24.4 351.9 15.2 356.8965517241379 15.2C 361.89310344827584 15.2 366.1758620689655 19.6 371.17241379310343 19.6C 376.16896551724136 19.6 380.451724137931 26 385.44827586206895 26C 390.4448275862069 26 394.72758620689655 23.6 399.7241379310345 23.6C 404.7206896551724 23.6 409.00344827586207 13.2 414 13.2C 414 13.2 414 13.2 414 40M 414 13.2z" fill="rgba(32,107,196,0.16)" fill-opacity="1" stroke-opacity="1" stroke-linecap="round" stroke-width="0" stroke-dasharray="0" class="apexcharts-area" index="0" clip-path="url(#gridRectMaskhwhojcwil)" pathTo="M 0 40L 0 25.2C 4.99655172413793 25.2 9.279310344827586 26 14.275862068965516 26C 19.272413793103446 26 23.555172413793102 22.4 28.551724137931032 22.4C 33.54827586206896 22.4 37.83103448275862 28.8 42.82758620689655 28.8C 47.82413793103448 28.8 52.106896551724134 25.6 57.103448275862064 25.6C 62.099999999999994 25.6 66.38275862068966 30.4 71.37931034482759 30.4C 76.37586206896552 30.4 80.65862068965517 14 85.6551724137931 14C 90.65172413793103 14 94.93448275862069 27.6 99.93103448275862 27.6C 104.92758620689655 27.6 109.2103448275862 25.2 114.20689655172413 25.2C 119.20344827586206 25.2 123.48620689655172 24.4 128.48275862068965 24.4C 133.47931034482758 24.4 137.76206896551724 15.2 142.75862068965517 15.2C 147.7551724137931 15.2 152.03793103448277 19.6 157.0344827586207 19.6C 162.03103448275863 19.6 166.31379310344826 26 171.3103448275862 26C 176.30689655172412 26 180.58965517241379 23.6 185.58620689655172 23.6C 190.58275862068965 23.6 194.8655172413793 26 199.86206896551724 26C 204.85862068965517 26 209.14137931034483 29.2 214.13793103448276 29.2C 219.1344827586207 29.2 223.41724137931033 2.799999999999997 228.41379310344826 2.799999999999997C 233.4103448275862 2.799999999999997 237.69310344827585 18.8 242.68965517241378 18.8C 247.6862068965517 18.8 251.96896551724137 15.600000000000001 256.9655172413793 15.600000000000001C 261.96206896551723 15.600000000000001 266.2448275862069 29.2 271.2413793103448 29.2C 276.23793103448276 29.2 280.5206896551724 18.4 285.51724137931035 18.4C 290.5137931034483 18.4 294.79655172413794 22.8 299.7931034482759 22.8C 304.7896551724138 22.8 309.07241379310346 32.4 314.0689655172414 32.4C 319.0655172413793 32.4 323.34827586206893 21.6 328.34482758620686 21.6C 333.3413793103448 21.6 337.62413793103445 24.4 342.6206896551724 24.4C 347.6172413793103 24.4 351.9 15.2 356.8965517241379 15.2C 361.89310344827584 15.2 366.1758620689655 19.6 371.17241379310343 19.6C 376.16896551724136 19.6 380.451724137931 26 385.44827586206895 26C 390.4448275862069 26 394.72758620689655 23.6 399.7241379310345 23.6C 404.7206896551724 23.6 409.00344827586207 13.2 414 13.2C 414 13.2 414 13.2 414 40M 414 13.2z" pathFrom="M -1 40L -1 40L 14.275862068965516 40L 28.551724137931032 40L 42.82758620689655 40L 57.103448275862064 40L 71.37931034482759 40L 85.6551724137931 40L 99.93103448275862 40L 114.20689655172413 40L 128.48275862068965 40L 142.75862068965517 40L 157.0344827586207 40L 171.3103448275862 40L 185.58620689655172 40L 199.86206896551724 40L 214.13793103448276 40L 228.41379310344826 40L 242.68965517241378 40L 256.9655172413793 40L 271.2413793103448 40L 285.51724137931035 40L 299.7931034482759 40L 314.0689655172414 40L 328.34482758620686 40L 342.6206896551724 40L 356.8965517241379 40L 371.17241379310343 40L 385.44827586206895 40L 399.7241379310345 40L 414 40"></path><path id="SvgjsPath1046" d="M 0 25.2C 4.99655172413793 25.2 9.279310344827586 26 14.275862068965516 26C 19.272413793103446 26 23.555172413793102 22.4 28.551724137931032 22.4C 33.54827586206896 22.4 37.83103448275862 28.8 42.82758620689655 28.8C 47.82413793103448 28.8 52.106896551724134 25.6 57.103448275862064 25.6C 62.099999999999994 25.6 66.38275862068966 30.4 71.37931034482759 30.4C 76.37586206896552 30.4 80.65862068965517 14 85.6551724137931 14C 90.65172413793103 14 94.93448275862069 27.6 99.93103448275862 27.6C 104.92758620689655 27.6 109.2103448275862 25.2 114.20689655172413 25.2C 119.20344827586206 25.2 123.48620689655172 24.4 128.48275862068965 24.4C 133.47931034482758 24.4 137.76206896551724 15.2 142.75862068965517 15.2C 147.7551724137931 15.2 152.03793103448277 19.6 157.0344827586207 19.6C 162.03103448275863 19.6 166.31379310344826 26 171.3103448275862 26C 176.30689655172412 26 180.58965517241379 23.6 185.58620689655172 23.6C 190.58275862068965 23.6 194.8655172413793 26 199.86206896551724 26C 204.85862068965517 26 209.14137931034483 29.2 214.13793103448276 29.2C 219.1344827586207 29.2 223.41724137931033 2.799999999999997 228.41379310344826 2.799999999999997C 233.4103448275862 2.799999999999997 237.69310344827585 18.8 242.68965517241378 18.8C 247.6862068965517 18.8 251.96896551724137 15.600000000000001 256.9655172413793 15.600000000000001C 261.96206896551723 15.600000000000001 266.2448275862069 29.2 271.2413793103448 29.2C 276.23793103448276 29.2 280.5206896551724 18.4 285.51724137931035 18.4C 290.5137931034483 18.4 294.79655172413794 22.8 299.7931034482759 22.8C 304.7896551724138 22.8 309.07241379310346 32.4 314.0689655172414 32.4C 319.0655172413793 32.4 323.34827586206893 21.6 328.34482758620686 21.6C 333.3413793103448 21.6 337.62413793103445 24.4 342.6206896551724 24.4C 347.6172413793103 24.4 351.9 15.2 356.8965517241379 15.2C 361.89310344827584 15.2 366.1758620689655 19.6 371.17241379310343 19.6C 376.16896551724136 19.6 380.451724137931 26 385.44827586206895 26C 390.4448275862069 26 394.72758620689655 23.6 399.7241379310345 23.6C 404.7206896551724 23.6 409.00344827586207 13.2 414 13.2" fill="none" fill-opacity="1" stroke="#206bc4" stroke-opacity="1" stroke-linecap="round" stroke-width="2" stroke-dasharray="0" class="apexcharts-area" index="0" clip-path="url(#gridRectMaskhwhojcwil)" pathTo="M 0 25.2C 4.99655172413793 25.2 9.279310344827586 26 14.275862068965516 26C 19.272413793103446 26 23.555172413793102 22.4 28.551724137931032 22.4C 33.54827586206896 22.4 37.83103448275862 28.8 42.82758620689655 28.8C 47.82413793103448 28.8 52.106896551724134 25.6 57.103448275862064 25.6C 62.099999999999994 25.6 66.38275862068966 30.4 71.37931034482759 30.4C 76.37586206896552 30.4 80.65862068965517 14 85.6551724137931 14C 90.65172413793103 14 94.93448275862069 27.6 99.93103448275862 27.6C 104.92758620689655 27.6 109.2103448275862 25.2 114.20689655172413 25.2C 119.20344827586206 25.2 123.48620689655172 24.4 128.48275862068965 24.4C 133.47931034482758 24.4 137.76206896551724 15.2 142.75862068965517 15.2C 147.7551724137931 15.2 152.03793103448277 19.6 157.0344827586207 19.6C 162.03103448275863 19.6 166.31379310344826 26 171.3103448275862 26C 176.30689655172412 26 180.58965517241379 23.6 185.58620689655172 23.6C 190.58275862068965 23.6 194.8655172413793 26 199.86206896551724 26C 204.85862068965517 26 209.14137931034483 29.2 214.13793103448276 29.2C 219.1344827586207 29.2 223.41724137931033 2.799999999999997 228.41379310344826 2.799999999999997C 233.4103448275862 2.799999999999997 237.69310344827585 18.8 242.68965517241378 18.8C 247.6862068965517 18.8 251.96896551724137 15.600000000000001 256.9655172413793 15.600000000000001C 261.96206896551723 15.600000000000001 266.2448275862069 29.2 271.2413793103448 29.2C 276.23793103448276 29.2 280.5206896551724 18.4 285.51724137931035 18.4C 290.5137931034483 18.4 294.79655172413794 22.8 299.7931034482759 22.8C 304.7896551724138 22.8 309.07241379310346 32.4 314.0689655172414 32.4C 319.0655172413793 32.4 323.34827586206893 21.6 328.34482758620686 21.6C 333.3413793103448 21.6 337.62413793103445 24.4 342.6206896551724 24.4C 347.6172413793103 24.4 351.9 15.2 356.8965517241379 15.2C 361.89310344827584 15.2 366.1758620689655 19.6 371.17241379310343 19.6C 376.16896551724136 19.6 380.451724137931 26 385.44827586206895 26C 390.4448275862069 26 394.72758620689655 23.6 399.7241379310345 23.6C 404.7206896551724 23.6 409.00344827586207 13.2 414 13.2" pathFrom="M -1 40L -1 40L 14.275862068965516 40L 28.551724137931032 40L 42.82758620689655 40L 57.103448275862064 40L 71.37931034482759 40L 85.6551724137931 40L 99.93103448275862 40L 114.20689655172413 40L 128.48275862068965 40L 142.75862068965517 40L 157.0344827586207 40L 171.3103448275862 40L 185.58620689655172 40L 199.86206896551724 40L 214.13793103448276 40L 228.41379310344826 40L 242.68965517241378 40L 256.9655172413793 40L 271.2413793103448 40L 285.51724137931035 40L 299.7931034482759 40L 314.0689655172414 40L 328.34482758620686 40L 342.6206896551724 40L 356.8965517241379 40L 371.17241379310343 40L 385.44827586206895 40L 399.7241379310345 40L 414 40"></path><g id="SvgjsG1043" class="apexcharts-series-markers-wrap" data:realIndex="0"><g class="apexcharts-series-markers"><circle id="SvgjsCircle1074" r="0" cx="0" cy="0" class="apexcharts-marker w376xkdwk no-pointer-events" stroke="#ffffff" fill="#206bc4" fill-opacity="1" stroke-width="2" stroke-opacity="0.9" default-marker-size="0"></circle></g></g></g><g id="SvgjsG1044" class="apexcharts-datalabels" data:realIndex="0"></g></g><line id="SvgjsLine1069" x1="0" y1="0" x2="414" y2="0" stroke="#b6b6b6" stroke-dasharray="0" stroke-width="1" stroke-linecap="butt" class="apexcharts-ycrosshairs"></line><line id="SvgjsLine1070" x1="0" y1="0" x2="414" y2="0" stroke-dasharray="0" stroke-width="0" stroke-linecap="butt" class="apexcharts-ycrosshairs-hidden"></line><g id="SvgjsG1071" class="apexcharts-yaxis-annotations"></g><g id="SvgjsG1072" class="apexcharts-xaxis-annotations"></g><g id="SvgjsG1073" class="apexcharts-point-annotations"></g></g><rect id="SvgjsRect1007" width="0" height="0" x="0" y="0" rx="0" ry="0" opacity="1" stroke-width="0" stroke="none" stroke-dasharray="0" fill="#fefefe"></rect><g id="SvgjsG1057" class="apexcharts-yaxis" rel="0" transform="translate(-18, 0)"></g><g id="SvgjsG1004" class="apexcharts-annotations"></g></svg><div class="apexcharts-legend" style="max-height: 20px;"></div><div class="apexcharts-tooltip apexcharts-theme-light"><div class="apexcharts-tooltip-title" style="font-family: inherit; font-size: 12px;"></div><div class="apexcharts-tooltip-series-group" style="order: 1;"><span class="apexcharts-tooltip-marker" style="background-color: rgb(32, 107, 196);"></span><div class="apexcharts-tooltip-text" style="font-family: inherit; font-size: 12px;"><div class="apexcharts-tooltip-y-group"><span class="apexcharts-tooltip-text-y-label"></span><span class="apexcharts-tooltip-text-y-value"></span></div><div class="apexcharts-tooltip-goals-group"><span class="apexcharts-tooltip-text-goals-label"></span><span class="apexcharts-tooltip-text-goals-value"></span></div><div class="apexcharts-tooltip-z-group"><span class="apexcharts-tooltip-text-z-label"></span><span class="apexcharts-tooltip-text-z-value"></span></div></div></div></div><div class="apexcharts-yaxistooltip apexcharts-yaxistooltip-0 apexcharts-yaxistooltip-left apexcharts-theme-light"><div class="apexcharts-yaxistooltip-text"></div></div></div></div>
              </div>
            </div>
            <div class="col-sm-4 col-lg-4">
              <div class="card">
                <div class="card-body">
                  <h3 class="card-title">Rank</h3>
                  <p class="text-muted">
                    Lorem ipsum dolor sit amet, consectetur adipisicing elit.
                    Aperiam deleniti fugit incidunt, iste, itaque minima neque
                    pariatur perferendis sed suscipit velit vitae voluptatem.
                  </p>
                </div>
              </div>
            </div>
            <div class="col-sm-4 col-lg-4">
              <div class="card">
                <div class="card-body">
                  <h3 class="card-title">Stats</h3>
                  <p class="text-muted">
                    Lorem ipsum dolor sit amet, consectetur adipisicing elit.
                    Aperiam deleniti fugit incidunt, iste, itaque minima neque
                    pariatur perferendis sed suscipit velit vitae voluptatem.
                  </p>
                </div>
              </div>
            </div>
            <div class="col-12">
              <h3 class="mb-3">Recent Games</h3>
              <div class="card">
                <div class="table-responsive">
                  <table class="table table-vcenter card-table">
                    <thead>
                      <tr>
                        <th>Victory</th>
                        <th>Champion</th>
                        <th>Teammates</th>
                        <th>KDA</th>
                        <th>Playing time</th>
                        <th>Date</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="index in 10" :key="index">
                        <td>Team Red</td>
                        <td>Foo Bar</td>
                        <td>
                          <span class="avatar avatar-xs avatar-rounded m-1" style="background-image: url(https://placekitten.com/32/32)" v-for="index in 5" :key="index"></span>
                        </td>
                        <td>1:20</td>
                        <td>200</td>
                        <td>05-24-2022</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'IndexPage',
}
</script>
