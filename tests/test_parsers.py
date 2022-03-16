""" Test parsers
"""
from src.parse.parsers import parse_lorecommendations


def test_parse_lorecommendations(tmpdir):
    file1 = tmpdir / "lorecommendations.txt"
    file1.write(lo_recommendations)
    recommendations: dict = parse_lorecommendations(str(file1), ['zr', 'o'], l_max=7, node_max=20)

    # Test the extremities of the file data
    assert recommendations['zr'][0, 0] == -667.991409275491
    assert recommendations['zr'][0, 20] == 471.219353640417
    assert recommendations['zr'][7, 0] == 12.6624776697611
    assert recommendations['zr'][7, 20] == 701.496871736980

    assert recommendations['o'][0, 0] == -18.1330196840195
    assert recommendations['o'][0, 20] == 811.108682051687
    assert recommendations['o'][7, 0] == 21.1582573272429
    assert recommendations['o'][7, 20] == 1115.85029887173


lo_recommendations = """Energy parameters
 ------------
 species           1
 l=           0
 n=           0  -667.991409275491     
 n=           1  -379.240253369951     
 n=           2  -14.2874442969234     
 n=           3  -1.38217813307027     
 n=           4   3.42536744493380     
 n=           5   11.8660719836892     
 n=           6   23.5636119957248     
 n=           7   38.2306288649451     
 n=           8   55.7263665351973     
 n=           9   75.9709788864888     
 n=          10   98.9139500066572     
 n=          11   124.514514588677     
 n=          12   152.743832883020     
 n=          13   183.579690781518     
 n=          14   217.003531335318     
 n=          15   253.000883235486     
 n=          16   291.559525401789     
 n=          17   332.669055583656     
 n=          18   376.320594999116     
 n=          19   422.506316266407     
 n=          20   471.219353640417     
 
 l=           1
 n=           0  -80.6288970845078     
 n=           1  -11.0903296755164     
 n=           2 -0.501589892294286     
 n=           3   4.26159803522064     
 n=           4   12.6765809910205     
 n=           5   24.1864348726792     
 n=           6   38.5622091557403     
 n=           7   55.6807569234608     
 n=           8   75.4735019827357     
 n=           9   97.8980259059199     
 n=          10   122.919966498227     
 n=          11   150.516651759929     
 n=          12   180.670780115227     
 n=          13   213.368376374010     
 n=          14   248.599071833936     
 n=          15   286.354093985085     
 n=          16   326.626195334648     
 n=          17   369.409303460139     
 n=          18   414.698205295194     
 n=          19   462.488553388670     
 n=          20   512.776715139228     
 
 l=           2
 n=           0  -5.84500670493726     
 n=           1  0.914547790113852     
 n=           2   5.64059751661934     
 n=           3   13.6826879756866     
 n=           4   24.5520764081153     
 n=           5   38.1279117157817     
 n=           6   54.3361196568741     
 n=           7   73.1447106535396     
 n=           8   94.5327917111786     
 n=           9   118.481063037598     
 n=          10   144.977912195015     
 n=          11   174.011967814267     
 n=          12   205.574098879777     
 n=          13   239.656984734903     
 n=          14   276.254028107871     
 n=          15   315.360043618080     
 n=          16   356.970704153000     
 n=          17   401.082480089301     
 n=          18   447.692451905333     
 n=          19   496.798038377992     
 n=          20   548.396871315060     
 
 l=           3
 n=           0   2.36543561629785     
 n=           1   6.65613297203595     
 n=           2   13.6859941886813     
 n=           3   23.4200580684237     
 n=           4   35.8130236114344     
 n=           5   50.8218822062476     
 n=           6   68.4323085048091     
 n=           7   88.6180461427449     
 n=           8   111.361136021387     
 n=           9   136.649045070290     
 n=          10   164.470347048785     
 n=          11   194.818035990892     
 n=          12   227.685641107760     
 n=          13   263.067948898846     
 n=          14   300.960513772017     
 n=          15   341.359086043891     
 n=          16   384.259846353525     
 n=          17   429.659229054574     
 n=          18   477.554065232093     
 n=          19   527.941644901146     
 n=          20   580.819713791749     
 
 l=           4
 n=           0   4.78327933801762     
 n=           1   11.1861394342653     
 n=           2   20.0549805610878     
 n=           3   31.4459143751536     
 n=           4   45.3932929111412     
 n=           5   61.8882775137132     
 n=           6   80.9243008810288     
 n=           7   102.502997236370     
 n=           8   126.615811828389     
 n=           9   153.256653605462     
 n=          10   182.418644353986     
 n=          11   214.095196547124     
 n=          12   248.281585578559     
 n=          13   284.973444242109     
 n=          14   324.167445305596     
 n=          15   365.860836088012     
 n=          16   410.051215463591     
 n=          17   456.736441304005     
 n=          18   505.914410791083     
 n=          19   557.583049904892     
 n=          20   611.740322451597     
 
 l=           5
 n=           0   7.19867764015665     
 n=           1   15.3621191123735     
 n=           2   25.8533071405062     
 n=           3   38.8031977822050     
 n=           4   54.2473517043863     
 n=           5   72.2045259377250     
 n=           6   92.6679005431248     
 n=           7   115.640428494746     
 n=           8   141.124034678391     
 n=           9   169.116569806891     
 n=          10   199.616853136762     
 n=          11   232.621614334552     
 n=          12   268.127679027327     
 n=          13   306.132119030021     
 n=          14   346.632055889954     
 n=          15   389.625130038242     
 n=          16   435.109311370510     
 n=          17   483.082945501847     
 n=          18   533.544669923608     
 n=          19   586.493284420762     
 n=          20   641.927651862646     
 
 l=           6
 n=           0   9.81038533179485     
 n=           1   19.6216060829818     
 n=           2   31.6227640307153     
 n=           3   46.0466116501745     
 n=           4   62.9275371080336     
 n=           5   82.2950688416822     
 n=           6   104.153660504068     
 n=           7   128.501360483987     
 n=           8   155.342520287142     
 n=           9   184.677822264788     
 n=          10   216.507751178548     
 n=          11   250.832405280892     
 n=          12   287.650469242525     
 n=          13   326.960599467696     
 n=          14   368.761122718885     
 n=          15   413.050297246437     
 n=          16   459.826489472715     
 n=          17   509.088174131056     
 n=          18   560.834044276091     
 n=          19   615.063010413319     
 n=          20   671.774187893929     
 
 l=           7
 n=           0   12.6624776697611     
 n=           1   24.0802985211897     
 n=           2   37.5388355337391     
 n=           3   53.3853157981699     
 n=           4   71.6647744403418     
 n=           5   92.4070922867511     
 n=           6   115.628862474925     
 n=           7   141.329587462520     
 n=           8   169.511522400961     
 n=           9   200.177408305896     
 n=          10   233.327910302679     
 n=          11   268.964323270499     
 n=          12   307.086991656717     
 n=          13   347.695645832420     
 n=          14   390.789800448397     
 n=          15   436.368601791598     
 n=          16   484.431079085582     
 n=          17   534.976180609759     
 n=          18   588.002837007884     
 n=          19   643.510037452071     
 n=          20   701.496871736980     
 
 species           2
 l=           0
 n=           0  -18.1330196840195     
 n=           1 -3.218920876138445E-002
 n=           2   5.81819501510778     
 n=           3   16.7150196872253     
 n=           4   31.9344551391894     
 n=           5   51.2561454695178     
 n=           6   74.5920412870563     
 n=           7   101.891889865373     
 n=           8   133.120968999725     
 n=           9   168.260906693085     
 n=          10   207.302968033433     
 n=          11   250.238963404836     
 n=          12   297.060844282271     
 n=          13   347.763393463586     
 n=          14   402.343419996870     
 n=          15   460.797943587475     
 n=          16   523.124161766010     
 n=          17   589.319926813159     
 n=          18   659.383565780216     
 n=          19   733.313588888199     
 n=          20   811.108682051687     
 
 l=           1
 n=           0  0.542669465536126     
 n=           1   5.30731652299547     
 n=           2   14.5900278687783     
 n=           3   28.0005216968489     
 n=           4   45.4547850173366     
 n=           5   66.8925110265213     
 n=           6   92.2699293853404     
 n=           7   121.567853598202     
 n=           8   154.778194692793     
 n=           9   191.889969147828     
 n=          10   232.892462132675     
 n=          11   277.780162162419     
 n=          12   326.549840165138     
 n=          13   379.197603598480     
 n=          14   435.719828550415     
 n=          15   496.114068842998     
 n=          16   560.378428122440     
 n=          17   628.511089551570     
 n=          18   700.510463959042     
 n=          19   776.375261225560     
 n=          20   856.104368533369     
 
 l=           2
 n=           0   3.54162855263558     
 n=           1   10.8404977381366     
 n=           2   22.3015353377704     
 n=           3   37.7990822058518     
 n=           4   57.2724512463783     
 n=           5   80.7017901676931     
 n=           6   108.067145356573     
 n=           7   139.344804293818     
 n=           8   174.521000462290     
 n=           9   213.591145984513     
 n=          10   256.550216578245     
 n=          11   303.391601611005     
 n=          12   354.110814115493     
 n=          13   408.705428235619     
 n=          14   467.173108282615     
 n=          15   529.511428428567     
 n=          16   595.718489082444     
 n=          17   665.792835922274     
 n=          18   739.733156308282     
 n=          19   817.538262233150     
 n=          20   899.207143140850     
 
 l=           3
 n=           0   6.31529232771970     
 n=           1   16.0396598388704     
 n=           2   29.6597498389934     
 n=           3   47.2461462642027     
 n=           4   68.7641250874585     
 n=           5   94.1978095073063     
 n=           6   123.544796683252     
 n=           7   156.798433080553     
 n=           8   193.946020150045     
 n=           9   234.978779534882     
 n=          10   279.893759287586     
 n=          11   328.688396034657     
 n=          12   381.358780668718     
 n=          13   437.901713844410     
 n=          14   498.315297622637     
 n=          15   562.597945658439     
 n=          16   630.748028273493     
 n=          17   702.764152164392     
 n=          18   778.645205340205     
 n=          19   858.390209926669     
 n=          20   941.998278051366     
 
 l=           4
 n=           0   9.40911270698223     
 n=           1   21.4662749969230     
 n=           2   37.2061516926422     
 n=           3   56.8499191380597     
 n=           4   80.3990863396830     
 n=           5   107.841273276560     
 n=           6   139.172875715499     
 n=           7   174.396177780324     
 n=           8   213.508934297378     
 n=           9   256.503894271916     
 n=          10   303.375524397416     
 n=          11   354.121859762977     
 n=          12   408.741432510570     
 n=          13   467.231883414338     
 n=          14   529.591030940959     
 n=          15   595.817428265865     
 n=          16   665.909916335067     
 n=          17   739.867350981294     
 n=          18   817.688711795101     
 n=          19   899.373147745203     
 n=          20   984.919911144370     
 
 l=           5
 n=           0   12.9021323357210     
 n=           1   27.2691844769492     
 n=           2   45.1132842352017     
 n=           3   66.7981838475503     
 n=           4   92.3624172048559     
 n=           5   121.806101538993     
 n=           6   155.124728866751     
 n=           7   192.319294106022     
 n=           8   233.393235116861     
 n=           9   278.345922351180     
 n=          10   327.173035752640     
 n=          11   379.871089566801     
 n=          12   436.438775576574     
 n=          13   496.875180278980     
 n=          14   561.178840212644     
 n=          15   629.348290311170     
 n=          16   701.382459633356     
 n=          17   777.280480522399     
 n=          18   857.041522434139     
 n=          19   940.664828944823     
 n=          20   1028.14974749840     
 
 l=           6
 n=           0   16.8161347573648     
 n=           1   33.4995416315504     
 n=           2   53.4462459347742     
 n=           3   77.1684283376427     
 n=           4   104.739942782253     
 n=           5   136.176990505111     
 n=           6   171.480131181057     
 n=           7   210.648572240789     
 n=           8   253.685176067296     
 n=           9   300.593397437316     
 n=          10   351.373265123331     
 n=          11   406.022176556170     
 n=          12   464.537961779861     
 n=          13   526.919768561318     
 n=          14   593.167008757674     
 n=          15   663.278758289362     
 n=          16   737.254041721202     
 n=          17   815.092085730109     
 n=          18   896.792242690137     
 n=          19   982.353899716896     
 n=          20   1071.77649267734     
 
 l=           7
 n=           0   21.1582573272429     
 n=           1   40.1780718485853     
 n=           2   62.2334186252010     
 n=           3   87.9956048690115     
 n=           4   117.573659692168     
 n=           5   151.000029762416     
 n=           6   188.283786182454     
 n=           7   229.426046186901     
 n=           8   274.428027535316     
 n=           9   323.293249618008     
 n=          10   376.024832114406     
 n=          11   432.623108773441     
 n=          12   493.086553729868     
 n=          13   557.413859104093     
 n=          14   625.604498663243     
 n=          15   697.658102200973     
 n=          16   773.574087252689     
 n=          17   853.351813824140     
 n=          18   936.990737829732     
 n=          19   1024.49038297874     
 n=          20   1115.85029887173     
 
 ------------"""
