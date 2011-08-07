<?php
$width = 600;
$half_w = $width / 2;
$height = 600;
$half_h = $height / 2;

#radius is radius (in points) of circle from which amplitudes will be added;
$radius = 200;

#multiplier so ring doesn't look crazy out of shape;
$multiplier = min($width, $height) / 4000;

#bezier width;
$bezier_width = $radius * .07;

#max movement;
$max_move = .6;

#DEBUG echo $multiplier;

#say the amp data is in data --- right now just test data;
$test_data_lims = 1000;
$data = array();
for ($p = 0; $p < $test_data_lims; $p++)
{
    $tmp = array();
    for ($x = 0; $x < 50; $x++)
    {
        $tmp[]=rand(0,255);
    }
    $data[]=$tmp;
}
#DEBUG print_r($data);

$im = new Imagick();
$draw = new ImagickDraw();
$dump = array();

#angle diff between each amplitude;
$angle_diff = pi()*2/count($data[0]);

$half_pi = pi() / 2;
$prevPoints = array();
foreach ($data as $f => $j)
{
    $im->newImage($width, $height, "black", "jpeg");
    $draw->setFillColor("white");
    $draw->pathStart();
    foreach ($j as $order => $amp)
    {
        #calculate angle for each freq
        $angle = $angle_diff * $order + $half_pi;

        #amplitude
        $newAmp = $j[$order] * $multiplier;

        #limit max_move;
    #    try:;
    #        if abs(prevPoints[order-1]["amp"] - newAmp) > max_move:;
    #            newAmp = prevPoints[order]["amp"] - max_move;
    #    except (IndexError):;
    #        pass;
    #;
        #set x and y coords;
        $x = $half_w + cos($angle) * ($radius + $newAmp);
        $y = $half_h + sin($angle) * ($radius + $newAmp);

        $prevPoints[]= array("x"=> $x, "y"=> $y, "amp" => $newAmp);

        if ($order == 0)
            {
                $draw->pathMoveToAbsolute($x,$y);
            }

        else
            {
               $prevangle = $angle_diff * ($order - 1) + $half_pi;
               $cp1x = $prevPoints[$order - 1]["x"] + cos($prevangle + $half_pi) * $bezier_width;
               $cp1y = $prevPoints[$order - 1]["y"] + sin($prevangle + $half_pi) * $bezier_width;
               $cp2x = $x + cos($angle - $half_pi) * $bezier_width;
               $cp2y = $y + sin($angle - $half_pi) * $bezier_width;
               $draw->pathCurveToAbsolute($cp1x, $cp1y, $cp2x, $cp2y, $x, $y);;
            }

        if ($order == count($j) - 1)
            {
                $prevangle = $angle;
                $angle = $half_pi;
                $cp1x = $x + cos($prevangle + $half_pi) * $bezier_width;
                $cp1y = $y + sin($prevangle + $half_pi) * $bezier_width;
                $cp2x = $prevPoints[0]["x"] +  $bezier_width;
                $cp2y = $prevPoints[0]["y"];
                $draw->pathCurveToAbsolute($cp1x, $cp1y, $cp2x, $cp2y, $prevPoints[0]["x"], $prevPoints[0]["y"]);
            }
    }
    $draw->pathClose();
    $im->drawImage($draw);
    //echo $im->getImageBlob();
    //echo $im;
    $dump[] = $im->getImageBlob();
    $draw->destroy();
    $im->destroy();
}
//exit(0);
foreach ($dump as $image)
{
    echo $image;
}
?>
