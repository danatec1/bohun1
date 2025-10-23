import { useState, useEffect } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "./components/ui/card";
import { Carousel, CarouselContent, CarouselItem, CarouselNext, CarouselPrevious, CarouselApi } from "./components/ui/carousel";
import { BarChart3, PieChart as PieChartIcon, AreaChart as AreaChartIcon, MapPin, Smile, Package, Menu, X } from "lucide-react";
import { Button } from "./components/ui/button";

interface ChartSyncInfo {
  last_updated: string;
  total_regions: number;
  data_years: string[];
  yearly_totals: {
    [key: string]: number;
  };
}

export default function App() {
  const [api, setApi] = useState<CarouselApi>();
  const [current, setCurrent] = useState(0);
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [syncInfo, setSyncInfo] = useState<ChartSyncInfo | null>(null);

  // 동기화 정보 로드
  useEffect(() => {
    const loadSyncInfo = async () => {
      try {
        const syncResponse = await fetch('/data/chart_sync_info.json');
        const syncData: ChartSyncInfo = await syncResponse.json();
        setSyncInfo(syncData);
      } catch (error) {
        console.log('동기화 정보 로드 실패:', error);
      }
    };
    
    loadSyncInfo();
  }, []);

  const charts = [
    {
      id: 0,
      title: "광역지자체별 연도별 위탁병원 현황",
      description: "광역지자체별 연도별 위탁병원 현황 통계 (MySQL 동기화)",
      icon: BarChart3,
      component: (
        <div className="space-y-4">
          <div className="rounded-lg overflow-hidden">
            <img 
              src="/data/images/1.JPG" 
              alt="광역지자체별 연도별 위탁병원 현황"
              className="w-full h-auto object-contain"
            />
          </div>
          <div className="text-sm text-muted-foreground space-y-2">
            <p>📊 광역지자체별 연도별 위탁병원 현황 통계 데이터를 보여주는 차트입니다.</p>
            {syncInfo && (
              <div className="mt-3 p-3 bg-muted rounded-lg">
                <p className="font-semibold text-foreground mb-1">🔄 MySQL 데이터 동기화 정보</p>
                <p>⏰ 마지막 업데이트: {syncInfo.last_updated}</p>
                <p>📍 광역지자체 수: {syncInfo.total_regions}개</p>
                <p className="mt-2">📈 연도별 전체 합계:</p>
                <div className="ml-4">
                  <p>• 2022년: {syncInfo.yearly_totals['2022']}개</p>
                  <p>• 2023년: {syncInfo.yearly_totals['2023']}개</p>
                  <p>• 2024년: {syncInfo.yearly_totals['2024']}개</p>
                </div>
              </div>
            )}
          </div>
        </div>
      ),
    },
    {
      id: 1,
      title: "전국 위탁병원 연도별 비율 분석",
      description: "전국 위탁병원 연도별 비율 파이 차트 (MySQL 동기화)",
      icon: PieChartIcon,
      component: (
        <div className="space-y-4">
          <div className="rounded-lg overflow-hidden">
            <img 
              src="/data/images/2.JPG" 
              alt="전국 위탁병원 연도별 비율 파이 차트"
              className="w-full h-auto object-contain"
            />
          </div>
          <div className="text-sm text-muted-foreground space-y-2">
            <p>🥧 전국 위탁병원 연도별 비율을 파이 차트로 보여주는 차트입니다.</p>
            {syncInfo && (
              <div className="mt-3 p-3 bg-muted rounded-lg">
                <p className="font-semibold text-foreground mb-1">🔄 MySQL 데이터 동기화 정보</p>
                <p>⏰ 마지막 업데이트: {syncInfo.last_updated}</p>
                <p className="mt-2">📊 연도별 비율:</p>
                <div className="ml-4">
                  {(() => {
                    const total = syncInfo.yearly_totals['2022'] + syncInfo.yearly_totals['2023'] + syncInfo.yearly_totals['2024'];
                    return (
                      <>
                        <p>• 2022년: {syncInfo.yearly_totals['2022']}개 ({((syncInfo.yearly_totals['2022'] / total) * 100).toFixed(1)}%)</p>
                        <p>• 2023년: {syncInfo.yearly_totals['2023']}개 ({((syncInfo.yearly_totals['2023'] / total) * 100).toFixed(1)}%)</p>
                        <p>• 2024년: {syncInfo.yearly_totals['2024']}개 ({((syncInfo.yearly_totals['2024'] / total) * 100).toFixed(1)}%)</p>
                        <p className="mt-2 font-semibold">총합: {total.toLocaleString()}개</p>
                      </>
                    );
                  })()}
                </div>
              </div>
            )}
          </div>
        </div>
      ),
    },
    {
      id: 2,
      title: "전국 위탁병원 연도, 월, 연월, 인원 상관관계 분석",
      description: "MySQL 실시간 데이터 기반 산점도 행렬 차트 (Scatter Matrix)",
      icon: PieChartIcon,
      component: (
        <div className="space-y-4">
          <iframe
            src="./chart3_scatter_matrix.html"
            width="100%"
            height="850px"
            style={{ border: 'none', borderRadius: '8px' }}
            title="전국 위탁병원 연도, 월, 연월, 인원 상관관계 분석"
          />
        </div>
      ),
    },

    {
      id: 3,
      title: "전국 위탁병원 연도별 월별 이용인원 추이",
      description: "MySQL 실시간 데이터 기반 연도별 비교 Area 차트",
      icon: AreaChartIcon,
      component: (
        <div className="space-y-4">
          <iframe
            src="./chart4_yearly_area.html"
            width="100%"
            height="650px"
            style={{ border: 'none', borderRadius: '8px' }}
            title="전국 위탁병원 연도별 월별 이용인원 추이"
          />
        </div>
      ),
    },
    {
      id: 4,
      title: "광역지자체별 연도별 위탁병원 이용인원",
      description: "MySQL 실시간 데이터 기반 지역별 분석 차트",
      icon: MapPin,
      component: (
        <div className="space-y-4">
          <div className="text-center p-8">
            <MapPin className="w-16 h-16 mx-auto mb-4 text-muted-foreground" />
            <p className="text-lg text-muted-foreground">지역별 차트 준비 중입니다</p>
            <p className="text-sm text-muted-foreground mt-2">광역지자체별 연도별 위탁병원 이용인원 데이터</p>
          </div>
        </div>
      ),
    },
    {
      id: 5,
      title: "광역지자체별 연도별 위탁병원 이용 인원",
      description: "MySQL 실시간 데이터 기반 광역지자체별 연도별 그룹 막대 차트 (2023년3월~2025년4월)",
      icon: Smile,
      component: (
        <div className="space-y-4">
          <iframe
            src="./chart5_regional_bar.html"
            width="100%"
            height="650px"
            style={{ border: 'none', borderRadius: '8px' }}
            title="광역지자체별 연도별 위탁병원 이용 인원"
          />
        </div>
      ),
    },
    {
      id: 6,
      title: "광역지자체별 이용 인원",
      description: "MySQL 실시간 데이터 기반 Pivot 막대 차트 (2023년3월~2025년4월)",
      icon: Package,
      component: (
        <div className="space-y-4">
          <iframe
            src="./chart6_pivot_bar.html"
            width="100%"
            height="650px"
            style={{ border: 'none', borderRadius: '8px' }}
            title="광역지자체별 이용 인원"
          />
        </div>
      ),
    },
    {
      id: 7,
      title: "연도별 광역지자체별 위탁병원 이용 인원 비율",
      description: "MySQL 실시간 데이터 기반 연도별 파이차트 서브플롯 (2023년3월~2025년4월)",
      icon: PieChartIcon,
      component: (
        <div className="space-y-4">
          <iframe
            src="./chart7_pie_subplots.html"
            width="100%"
            height="1050px"
            style={{ border: 'none', borderRadius: '8px' }}
            title="연도별 광역지자체별 위탁병원 이용 인원 비율 파이차트"
          />
        </div>
      ),
    },
  ];

  const handleMenuClick = (index: number) => {
    api?.scrollTo(index);
    // 모바일에서는 메뉴 클릭 시 사이드바 자동으로 닫기
    if (window.innerWidth < 1024) {
      setSidebarOpen(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <div className="flex h-screen relative">
        {/* Overlay for mobile */}
        {sidebarOpen && (
          <div
            className="fixed inset-0 bg-black/50 z-30 lg:hidden"
            onClick={() => setSidebarOpen(false)}
          />
        )}

        {/* Left Sidebar - Always visible on desktop */}
        <div
          className={`w-64 border-r border-gray-700 overflow-y-auto h-screen z-40 shadow-2xl flex flex-col
            ${sidebarOpen ? "fixed lg:relative translate-x-0" : "fixed -translate-x-full lg:relative lg:translate-x-0"}`}
          style={{ backgroundColor: '#212529' }}
        >
          {/* Sidebar Header */}
          <div className="flex-shrink-0 p-6 pb-4 border-b" style={{ backgroundColor: '#212529', borderColor: '#343a40' }}>
            <div className="flex items-start justify-between gap-4 mb-2">
              <div className="flex-1 pt-1">
                <h1 className="text-xl font-bold" style={{ color: '#ffffff' }}>대시보드</h1>
                <p className="mt-1 text-sm" style={{ color: '#adb5bd' }}>차트를 선택하여 자세히 확인하세요</p>
              </div>
              {/* Mobile Close Button */}
              <Button
                size="icon"
                className="lg:hidden shadow-md flex-shrink-0 border-none"
                style={{ backgroundColor: '#343a40', color: '#ffffff' }}
                onClick={() => setSidebarOpen(false)}
              >
                <X className="h-5 w-5" />
              </Button>
            </div>
          </div>

          {/* Navigation Menu */}
          <nav className="flex flex-col flex-1 p-0 overflow-y-auto">
            {charts.map((chart, index) => {
              const Icon = chart.icon;
              const isActive = current === index;
              return (
                <button
                  key={chart.id}
                  onClick={() => handleMenuClick(index)}
                  className="w-full flex items-center gap-3 px-5 py-4 transition-all duration-200 border-l-4"
                  style={{
                    backgroundColor: isActive ? '#0d6efd' : 'transparent',
                    color: isActive ? '#ffffff' : '#dee2e6',
                    borderLeftColor: isActive ? '#0d6efd' : 'transparent',
                  }}
                  onMouseEnter={(e) => {
                    if (!isActive) {
                      e.currentTarget.style.backgroundColor = '#343a40';
                      e.currentTarget.style.color = '#ffffff';
                    }
                  }}
                  onMouseLeave={(e) => {
                    if (!isActive) {
                      e.currentTarget.style.backgroundColor = 'transparent';
                      e.currentTarget.style.color = '#dee2e6';
                    }
                  }}
                >
                  <Icon className="w-5 h-5 flex-shrink-0" />
                  <div className="flex-1 text-left">
                    <div className="text-sm">{chart.title}</div>
                  </div>
                </button>
              );
            })}
          </nav>
        </div>

        {/* Right Content Area */}
        <div className="flex-1 flex flex-col overflow-hidden">
          {/* Mobile Header with Hamburger */}
          <div className="lg:hidden sticky top-0 bg-white border-b p-4 flex items-center gap-4 z-20 shadow-sm flex-shrink-0">
            <Button
              size="icon"
              className="bg-gray-900 hover:bg-blue-600 text-white border-none"
              onClick={() => setSidebarOpen(true)}
            >
              <Menu className="h-5 w-5" />
            </Button>
            <h1 className="text-lg font-bold text-gray-900">데이터 분석 대시보드</h1>
          </div>

          <div className="flex-1 overflow-y-auto p-8">
            <Carousel
              setApi={setApi}
              className="w-full h-full"
              opts={{
                align: "start",
                loop: true,
              }}
              orientation="vertical"
              onInit={(carousel) => {
                setCurrent(carousel.selectedScrollSnap());
                carousel.on("select", () => {
                  setCurrent(carousel.selectedScrollSnap());
                });
              }}
            >
              <CarouselContent className="h-[calc(100vh-8rem)]">
                {charts.map((chart) => (
                  <CarouselItem key={chart.id}>
                    <Card className="h-full flex flex-col">
                      <CardHeader>
                        <CardTitle>{chart.title}</CardTitle>
                        <CardDescription>{chart.description}</CardDescription>
                      </CardHeader>
                      <CardContent className="flex-1 flex items-center justify-center overflow-y-auto">
                        {chart.component}
                      </CardContent>
                    </Card>
                  </CarouselItem>
                ))}
              </CarouselContent>
              <div className="absolute right-8 top-1/2 -translate-y-1/2 flex flex-col gap-2">
                <CarouselPrevious className="relative inset-0 translate-x-0 translate-y-0" />
                <CarouselNext className="relative inset-0 translate-x-0 translate-y-0" />
              </div>
            </Carousel>

            {/* Carousel Indicator */}
            <div className="mt-4 flex justify-center gap-2">
              {charts.map((_, index) => (
                <button
                  key={index}
                  onClick={() => handleMenuClick(index)}
                  className={`h-2 rounded-full transition-all ${
                    current === index ? "w-8 bg-primary" : "w-2 bg-muted-foreground/30"
                  }`}
                />
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}