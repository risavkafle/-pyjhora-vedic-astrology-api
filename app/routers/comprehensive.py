"""Comprehensive analysis endpoint - All data in one call"""

from fastapi import APIRouter, HTTPException
from app.models.schemas import ChartRequest, ErrorResponse
from app.services.calculator import PyJHoraCalculator

router = APIRouter(prefix="/api/v1/comprehensive", tags=["Comprehensive Analysis"])

@router.post("/full-analysis", responses={400: {"model": ErrorResponse}})
async def get_full_analysis(request: ChartRequest):
    """
    Get Complete Vedic Astrology Analysis in One Call

    Returns:
    - All Divisional Charts (D1, D2, D3, D4, D7, D9, D10, D12, D16, D20, D24, D27, D30, D40, D45, D60)
    - Maha Dasha & Bhukti (Vimsottari)
    - Ashtakavarga (Bhinna & Sarva)
    - Shadbala (Planetary Strengths)
    - Bhava Bala (House Strengths)
    - Panchanga (Tithi, Vara, Nakshatra, Yoga, Karana)
    - Special Lagnas (Hora, Ghati, etc.)
    - All Yogas & Doshas

    This endpoint combines all major calculations into a single response.
    """
    try:
        calculator = PyJHoraCalculator(
            request.birth_data.dict(),
            request.ayanamsa
        )

        # Calculate all divisional charts
        from app.services.calculator import CHART_FACTORS
        all_charts = {}
        for chart_id in CHART_FACTORS.keys():
            chart_result = calculator.calculate_chart(chart_id)
            all_charts[chart_id.lower()] = {
                "name": f"{chart_id} - {chart_result.get('chart_type', chart_id)}",
                "ascendant": chart_result.get('ascendant'),
                "planets": chart_result.get('planets', [])
            }

        # Calculate Maha Dasha
        maha_dasha = calculator.calculate_dasha('VIMSOTTARI')

        # Calculate Antardasha (Bhukti)
        antardasha = calculator.calculate_dasha_bhukti('VIMSOTTARI')

        # Calculate Ashtakavarga (7 Bhinna + 1 Sarva)
        ashtakavarga = calculator.calculate_ashtakavarga()

        # Calculate Shadbala & Bhava Bala
        shadbala = calculator.calculate_shadbala()
        bhava_bala = calculator.calculate_bhava_bala()

        # Calculate Panchanga & Special Lagnas
        panchanga = calculator.calculate_panchanga()
        special_lagnas = calculator.calculate_special_lagnas()

        # Calculate Yogas & Doshas
        yogas = calculator.calculate_yogas()
        doshas = calculator.calculate_doshas()

        # Compile comprehensive response
        response = {
            "status": "success",
            "birth_data": request.birth_data.dict(),
            "ayanamsa": request.ayanamsa,

            "charts": all_charts,

            "dashas": {
                "system": "Vimsottari",
                "moon_nakshatra": maha_dasha.get('moon_nakshatra', {}),
                "maha_dasha": {
                    "periods": maha_dasha.get('maha_dasha_periods', []),
                    "current_period": maha_dasha.get('current_dasha')
                },
                "bhukti": {
                    "total_periods": len(antardasha.get('bhukti_periods', [])),
                    "periods": antardasha.get('bhukti_periods', []),
                    "current_period": antardasha.get('current_bhukti'),
                    "description": "Sub-periods (Antar Dasha) within the Maha Dasha"
                }
            },

            "ashtakavarga": {
                "bhinna_ashtakavarga": {
                    "description": "7 Individual Planet Charts (Bindu strength by house)",
                    "planets": ashtakavarga.get('binna_ashtakavarga', {})
                },
                "sarvashtakavarga": {
                    "description": "Combined Ashtakavarga (Total strength across all planets)",
                    "data": ashtakavarga.get('samudhaya_ashtakavarga', {})
                }
            },

            "strength": {
                "shadbala": shadbala.get('planetary_strengths', []),
                "bhava_bala": bhava_bala.get('house_strengths', []),
                "strongest_house": bhava_bala.get('strongest_house'),
                "weakest_house": bhava_bala.get('weakest_house')
            },

            "panchanga": panchanga,
            "special_lagnas": special_lagnas.get('special_lagnas', {}),

            "yogas": {
                "total_analyzed": len(yogas.get('yogas', [])),
                "total_present": sum(1 for y in yogas.get('yogas', []) if y.get('present', False)),
                "present_yogas": [y for y in yogas.get('yogas', []) if y.get('present', False)],
                "all_yogas": yogas.get('yogas', [])
            },

            "doshas": {
                "total_analyzed": len(doshas.get('doshas', [])),
                "total_present": sum(1 for d in doshas.get('doshas', []) if d.get('present', False)),
                "present_doshas": [d for d in doshas.get('doshas', []) if d.get('present', False)],
                "all_doshas": doshas.get('doshas', [])
            },

            "summary": {
                "charts_calculated": list(all_charts.keys()),
                "total_charts": len(all_charts),
                "panchanga_ready": True,
                "shadbala_ready": True,
                "yogas_present": sum(1 for y in yogas.get('yogas', []) if y.get('present', False)),
                "doshas_present": sum(1 for d in doshas.get('doshas', []) if d.get('present', False))
            }
        }

        return response

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
