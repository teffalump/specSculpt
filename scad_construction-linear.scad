function BEZ03(u) = pow((1-u), 3);
function BEZ13(u) = 3*u*(pow((1-u),2));
function BEZ23(u) = 3*(pow(u,2))*(1-u);
function BEZ33(u) = pow(u,3);

function PointAlongBez4(p0, p1, p2, p3, u) = [
	BEZ03(u)*p0[0]+BEZ13(u)*p1[0]+BEZ23(u)*p2[0]+BEZ33(u)*p3[0],
	BEZ03(u)*p0[1]+BEZ13(u)*p1[1]+BEZ23(u)*p2[1]+BEZ33(u)*p3[1]];

module BezStrip ()
{
amps = [1,30,4,1,45, 1];
length = 6;
max_length = 100;
step_length = max_length/(length-1);
min_radius = 1;
steps =100;
for (order = [0:length-2] )
	{
		assign(
				prevy=order*step_length,
				prevx=min_radius + amps[order],
				y = (order+1)*step_length,
				x = amps[order+1] + min_radius,
				cp1y = (order+.8)*step_length,
				cp1x = amps[order] + min_radius,
				cp2y = (order+ .2 )*step_length,
				cp2x = amps[order + 1] + min_radius

				
			)
		{
			for (step = [1:steps])
            {
                    assign (
                            initial_point=PointAlongBez4([prevx,prevy], [cp1x,cp1y], [cp2x,cp2y], [x,y], (step-1)/steps),
                            end_point=PointAlongBez4([prevx,prevy], [cp1x,cp1y], [cp2x,cp2y], [x,y], step/steps)
                            )
				{
					polygon(
						points = [[0,(step/steps + order)*step_length], 
                                    [0, (order + (step - 1)/steps) * step_length],
                                    initial_point, 
                                    end_point,
                                    step/steps) ]
						);
				}
            }
        }
	}
}
//linear_extrude(height=1) BezStrip();
//BezStrip()
rotate_extrude($fn=100) BezStrip();
