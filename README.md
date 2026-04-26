# Hands-On Koordinasi SKT

Nama: Izzah Faiq Putri Madani
NIM: 235150201111047

## **Lab 1 – Simulasi Lamport Clock**
1. Jalankan kode lab1_lamport.py, amati output
![image](https://hackmd.io/_uploads/B1WacuiTZg.png)

2. Gambar diagram event timeline P1, P2, P3 dengan
![image](https://hackmd.io/_uploads/Hyp_0KjTbl.png)


3. Jawab 4 pertanyaan di slide berikutnya secara tertulis
* Apakah t(SEND) selalu lebih kecil dari t(RECV)? Mengapa?
Ya, dalam sistem yang menggunakan algoritma Lamport Clock, nilai timestamp pada saat pengiriman ($t_{\text{send}}$) akan selalu lebih kecil daripada nilai timestamp saat pesan tersebut diterima ($t_{\text{recv}}$). Hal ini dikarenakan pada aturan pembaruan logical clock (Rule 2) yang menyatakan bahwa ketika suatu proses menerima pesan dengan timestamp $t_m$, proses penerima harus memperbarui local clock-nya menjadi $L_i = \max(L_i, t_m) + 1$. Penambahan nilai $+1$ ini menjamin secara matematis bahwa kejadian penerimaan pesan selalu terjadi "setelah" kejadian pengiriman pesan. Secara intuitif, sebuah pesan tidak mungkin diterima sebelum ia dikirimkan, sehingga algoritma ini secara konsisten menjaga urutan kausalitas tersebut.

* Apakah bisa disimpulkan P1.start terjadi sebelum P3.done? Jelaskan dengan relasi happened-before!
Berdasarkan pengamatan saya, dapat disimpulkan bahwa kejadian P1.start secara kausal terjadi sebelum P3.done melalui rantai relasi happened-before ($\to$). Sesuai dengan hukum transitivitas yang dikemukakan oleh Leslie Lamport, hubungan ini dapat dibuktikan melalui rangkaian kejadian yang saling terhubung. Dimulai dari urutan lokal di P1 di mana P1.start mendahului pengiriman pesan 'hello', yang kemudian diterima oleh P2 sehingga menciptakan relasi antar proses. Selanjutnya, di dalam P2 sendiri, penerimaan pesan tersebut memicu kejadian lokal berikutnya hingga akhirnya P2 mengirimkan pesan 'data' ke P3. Setelah P3 menerima pesan tersebut, barulah kejadian P3.done tercatat. Karena terdapat jalur kausalitas yang tidak terputus dari awal hingga akhir ($P1.start \to \dots \to P3.done$), maka secara logis dapat dipastikan bahwa P1.start memiliki hubungan happened-before terhadap P3.done. Dalam konteks sistem terdistribusi, hal ini menegaskan bahwa P1.start bertindak sebagai penyebab (cause) yang secara tidak langsung mengarah pada eksekusi akhir di P3.done.

* Jika P2 crash setelah mengirim 'ack' ke P1 tapi sebelum 'data' ke P3 — apa yang terjadi pada clock P3?
Modifikasi kode: ganti LamportClock dengan VectorClock. Tunjukkan hasilnya!
![image](https://hackmd.io/_uploads/r1BNFuiTWe.png)
Apabila terjadi kegagalan sistem (crash) pada P2 tepat setelah pengiriman pesan 'ack' namun sebelum pesan 'data' sempat dikirimkan ke P3, maka proses P3 akan mengalami kondisi stuck atau menunggu secara permanen (infinite waiting). Hal ini disebabkan karena dalam arsitektur sistem terdistribusi yang kita simulasikan, P3 bersifat pasif dan bergantung sepenuhnya pada pesan masuk dari P2 untuk memicu pembaruan logical clock-nya. Secara teknis, karena instruksi receive() pada P3 tidak pernah mendapatkan kiriman data, nilai timestamp pada P3 tidak akan pernah beranjak dari angka t=0. Dampak lebih luas dari kejadian ini adalah terputusnya rantai kausalitas Lamport; kejadian P3.done yang seharusnya memiliki urutan logis setelah kejadian-kejadian di P1 dan P2 tidak akan pernah tercapai. Dengan demikian, crash pada node perantara seperti P2 mengakibatkan hilangnya sinkronisasi waktu global dan kegagalan dalam melengkapi urutan kejadian happened-before di seluruh sistem.

4. Tambahkan proses P4, kirim pesan dari P3 ke P4 — catat hasilnya
![image](https://hackmd.io/_uploads/H1Ho9di6Ze.png)
Penambahan proses P4 ke dalam sistem menunjukkan bagaimana algoritma Lamport Clock menjaga konsistensi waktu saat terjadi interaksi antar-proses yang lebih kompleks. Setelah P3 menyelesaikan event lokalnya pada t=8, P3 mengirimkan pesan 'final_report' yang memicu kenaikan timestamp menjadi t=9. Ketika pesan tersebut diterima oleh P4, terjadi pembaruan logical clock menggunakan aturan $max(local, remote) + 1$, sehingga P4 mencatat kejadian penerimaan pada t=10. Event internal terakhir di P4, yaitu 'archive', kemudian tercatat pada t=11. Hal ini membuktikan bahwa penambahan node baru tetap menjamin relasi happened-before ($\to$) di mana kejadian di awal rantai (P1) secara logis tetap mendahului kejadian di akhir rantai (P4), meskipun jumlah proses dalam sistem terdistribusi bertambah.

## **Lab 2 – ZooKeeper CLI Praktikum**
1. Jalankan ZooKeeper via Docker, masuk ke zkCli.sh
![image](https://hackmd.io/_uploads/HJI1oOjTZl.png)
![image](https://hackmd.io/_uploads/S1RNjOjabx.png)

2. Buat ZNode /mahasiswa/[NIM], isi dengan nama Anda
![image](https://hackmd.io/_uploads/SyGz3_i6Wx.png)

3. Buka 2 terminal: satu watch /mahasiswa/[NIM], satu lagi ubah nilainya — screenshot notifikasi!
![Screenshot 2026-04-26 185028](https://hackmd.io/_uploads/HkY0MqiT-g.png)

4. Buat ephemeral node, lalu tutup koneksi. Buktikan node hilang!
![image](https://hackmd.io/_uploads/S1pxa_iabe.png)
![image](https://hackmd.io/_uploads/BJxx6ui6Zl.png)
![image](https://hackmd.io/_uploads/Syio6OsTWl.png)

## **Lab 2 – ZooKeeper: Distributed Lock (Tugas Inti)**
1. Jalankan kode di atas, amati urutan output — apakah hanya 1 worker di CR?
![image](https://hackmd.io/_uploads/SkD00dspbg.png)
Hasil eksekusi program menunjukkan keberhasilan mekanisme Mutual Exclusion yang dikelola oleh ZooKeeper, di mana terbukti hanya terdapat satu worker yang menempati Critical Region (CR) dalam satu interval waktu. Meskipun Worker-0, Worker-1, dan Worker-2 melakukan permintaan lock secara simultan, ZooKeeper secara konsisten memberikan akses secara eksklusif dan sekuensial. Melalui log program, dapat diobservasi bahwa setiap unit kerja harus menyelesaikan prosesnya dan melepaskan lock secara formal sebelum antrean berikutnya diizinkan untuk mengakses sumber daya tersebut.

2. Ubah jumlah worker menjadi 5. Apakah urutan selalu sama? Mengapa?
![image](https://hackmd.io/_uploads/rkfq1Ks6-g.png)
Urutan akses Critical Region tidak selalu berurutan (misal: Worker-1 lalu Worker-0) karena sifat thread scheduling. Meskipun ZooKeeper menggunakan prinsip FIFO, urutan eksekusi tetap bergantung pada processor scheduling yang menentukan thread mana yang lebih dulu berhasil mengirimkan permintaan ke server.

3. Simulasikan worker yang crash di tengah critical section (tambahkan raise Exception di dalam with lock). Apa yang terjadi pada worker lain?
![image](https://hackmd.io/_uploads/Sy2exFjTZg.png)
Kegagalan pada Worker-1 saat berada di dalam Critical Region terbukti tidak menghambat operasional sistem secara keseluruhan. Berkat penggunaan ephemeral node pada ZooKeeper, koneksi yang terputus akibat crash memicu penghapusan otomatis pada lock node terkait. Mekanisme ini secara efektif mencegah terjadinya deadlock, sehingga worker lain dalam antrean tetap dapat memperoleh akses secara berurutan tanpa intervensi manual.

4. Ganti Lock dengan implementasi manual menggunakan ephemeral sequential node. Hint: gunakan pola /lock/node- + cek sibling terkecil
![image](https://hackmd.io/_uploads/HJVWSqj6Wl.png)
Hasil observasi mengonfirmasi bahwa ZooKeeper berhasil mengelola antrean akses secara terstruktur. Setiap worker memasuki Critical Region secara sekuensial, mengikuti urutan nomor identitas unik yang dihasilkan secara otomatis oleh sistem penomoran znode milik ZooKeeper.

## **Lab 3 – Observasi Raft Consensus**
1. Buka browser ke https://raft.github.io/
![image](https://hackmd.io/_uploads/H1sxWKspZg.png)
2. Tunggu hingga leader terpilih — catat berapa lama (term berapa?)
![image](https://hackmd.io/_uploads/Hk5KzFsa-g.png)
![image](https://hackmd.io/_uploads/B14czYspbl.png)
Berdasarkan hasil observasi simulasi, Server 4 berhasil mencapai konsensus dan terpilih sebagai Leader pada term ke-2.

3. Klik Stop pada leader → amati re-election. Screenshot!
![image](https://hackmd.io/_uploads/Hys5fFi6Wx.png)
![image](https://hackmd.io/_uploads/rkbBQKs6-e.png)
Ketika operasional Server 4 dihentikan, sistem langsung memicu proses re-election yang berujung pada terpilihnya Server 3 sebagai leader baru untuk term ke-3.

4. Kirim beberapa log entry via tombol Request — amati replikasi ke follower
![image](https://hackmd.io/_uploads/S1NwmFspWe.png)
![image](https://hackmd.io/_uploads/B1X5XKiabg.png)
Dalam proses replikasi, Leader memanfaatkan pesan AppendEntries untuk mengirimkan log ke para Follower. Status log akan tetap uncommitted sampai konsensus tercapai; setelah mayoritas server memberikan respon positif, Leader akan menandai log tersebut sebagai committed untuk memastikan integritas data di seluruh sistem terdistribusi.

5. Aktifkan Network Partition → apa yang terjadi pada minority partition?
![image](https://hackmd.io/_uploads/H1UsNYi6Ze.png)
Dalam kondisi minority partition, server-server yang terisolasi akan kehilangan koneksi dengan Leader sehingga pengiriman heartbeat terhenti. Hal ini memicu mekanisme timeout yang memaksa node-node tersebut untuk berulang kali memulai proses Leader Election dan secara progresif menaikkan angka Term. Namun, dikarenakan jumlah node dalam partisi tersebut tidak memenuhi kuorum (syarat mayoritas), proses pemilihan akan selalu gagal dan sistem terjebak dalam siklus election yang tidak berujung. Begitu partisi jaringan pulih, protokol Raft akan mendeteksi adanya angka Term yang lebih tinggi, yang secara otomatis memaksa Leader lama untuk turun jabatan (step down) menjadi Follower. Proses ini diakhiri dengan sinkronisasi otoritas dan nilai term di seluruh server guna mengikuti angka term tertinggi yang ditemukan dalam sistem.

### Pertanyaan
1. Pada saat re-election, apakah node dengan log yang lebih pendek bisa jadi leader? Mengapa?
Dalam protokol Raft, sebuah node dengan log yang lebih pendek tidak akan bisa memenangkan pemilihan menjadi Leader. Hal ini dikarenakan Raft menerapkan aturan Election Restriction yang sangat ketat, di mana seorang Candidate hanya akan diberikan suara oleh pemilih (Voter) jika log miliknya setidaknya sama mutakhirnya (up-to-date) dengan milik pemilih tersebut. Mekanisme ini bertujuan untuk menjamin keamanan (safety) data, sehingga entri log yang sudah berstatus committed pada Term sebelumnya tidak akan pernah tertimpa atau hilang akibat kepemimpinan node yang tidak memiliki data lengkap.

2. Berapa minimum server yang harus aktif agar sistem tetap berfungsi (dari 5 server)?
Untuk memastikan sistem tetap berfungsi secara normal dalam klaster yang terdiri dari 5 server, diperlukan minimal 3 server yang aktif dan saling terhubung. Hal ini merujuk pada konsep kuorum atau mayoritas sederhana yang dirumuskan dengan $\lfloor N/2 \rfloor + 1$. Syarat mayoritas ini sangat krusial karena tanpa kehadiran minimal 3 node, sistem tidak akan mampu mencapai konsensus dalam proses pemilihan Leader maupun dalam melakukan commit terhadap log baru, sehingga sistem akan berhenti melayani permintaan write demi menjaga konsistensi.

3. Apa yang terjadi pada entry yang belum commit saat leader crash?
Apabila seorang Leader mengalami kegagalan (crash) sebelum sempat melakukan commit pada suatu entri log, maka entri tersebut akan tetap berada dalam status uncommitted dan belum dianggap sebagai bagian dari state sistem yang permanen. Saat Leader baru terpilih, ia akan mengambil alih kendali dan memaksa log pada seluruh Follower untuk sinkron dengan miliknya. Akibatnya, entri uncommitted dari Leader lama yang belum tereplikasi ke mayoritas node kemungkinan besar akan dihapus atau ditimpa oleh entri baru dari Leader yang baru, sesuai dengan prinsip konsistensi log pada algoritma Raft.

4. Bandingkan dengan ZooKeeper: siapa yang handle write saat leader down?
Berbeda dengan sistem tanpa koordinasi, pada ZooKeeper (ZAB Protocol), tidak ada node lain yang dapat menangani operasi write secara langsung ketika Leader sedang down. Sama halnya dengan Raft, ZooKeeper sangat bergantung pada keberadaan Leader yang valid untuk mengoordinasikan seluruh pembaruan data. Jika Leader mengalami kegagalan, sistem akan segera menghentikan pemrosesan seluruh permintaan modifikasi (write) dan memasuki fase recovery untuk memilih Leader baru. Layanan write hanya akan tersedia kembali setelah Leader baru terpilih dan berhasil melakukan sinkronisasi state dengan mayoritas Follower.

## **Lab 3 – etcd sebagai Raft-based KV Store**
1. Tambahkan watcher untuk key /config/timeout secara paralel.
![image](https://hackmd.io/_uploads/B1o9Dqopbe.png)

2. Implementasikan leader election dengan 2 node berbeda — siapa yang menang jika keduanya campaign bersamaan?
![image](https://hackmd.io/_uploads/HkMTPcsTWl.png)
Berdasarkan hasil pengujian pada Tugas 2, ketika Node-1 dan Node-2 melakukan campaign atau mencoba menjadi pemimpin secara bersamaan, pemenang ditentukan oleh siapa yang lebih dahulu berhasil melakukan operasi put_if_not_exists pada path /election/leader di server etcd. Meskipun secara kode keduanya dipicu hampir di waktu yang sama menggunakan threading, pada level backend, etcd memanfaatkan algoritma konsensus Raft untuk memastikan bahwa hanya ada satu permintaan yang diproses sebagai operasi atomik pertama. Oleh karena itu, node yang permintaan paketnya tiba di server beberapa milidetik lebih awal akan berhasil menduduki jabatan Leader, sementara node lainnya akan masuk ke kondisi looping atau menunggu hingga path tersebut dihapus (melakukan resign) oleh pemimpin yang sedang menjabat.

3. Catat output dan jelaskan mengapa hasilnya deterministik atau tidak.
![image](https://hackmd.io/_uploads/S15GuFspZg.png)
* watcher : berdasarkan log yang dihasilkan, mekanisme Watcher pada etcd terbukti mampu menangkap setiap perubahan pada kunci /config/threshold dan /config/timeout secara real-time. Hasil ini menunjukkan bahwa modifikasi menggunakan multithreading berhasil menjalankan dua proses pengawasan secara independen, di mana setiap kali instruksi put dijalankan, Watcher terkait langsung memberikan notifikasi berupa PutEvent. Hal ini mengonfirmasi bahwa etcd secara efektif mendistribusikan pembaruan data dari server kepada seluruh client yang berlangganan pada key tertentu tanpa ada data yang terlewat, meskipun pembaruan dilakukan pada dua lokasi konfigurasi yang berbeda secara nyaris bersamaan.
* leader election : meskipun Node-1 dan Node-2 memulai proses campaign secara simultan, hasil akhir dari pemilihan pemimpin ini tetap bersifat deterministik dalam hal eksklusivitas, namun non-deterministik dalam hal urutan pemenang. Dikatakan deterministik karena mekanisme put_if_not_exists pada etcd menjamin bahwa hanya satu node yang bisa menduduki posisi Leader pada satu waktu (terlihat dari Node-1 yang menang lebih dulu, baru kemudian Node-2 menyusul setelah Node-1 resign). Namun, urutan siapa yang menang terlebih dahulu bersifat non-deterministik karena sangat bergantung pada faktor eksternal seperti CPU scheduling dan latensi jaringan saat paket permintaan sampai ke server. Dalam sistem terdistribusi, kepastian bahwa "hanya ada satu pemenang" jauh lebih krusial daripada urutan kemenangannya untuk menjaga konsistensi sistem.

## **Lab 4 – Vector Clock: Implementasi & Analisis**
1. Jalankan kode, verifikasi output a → b = True
![image](https://hackmd.io/_uploads/SynoOYoa-g.png)
Hasil verifikasi a -> b bernilai True karena setiap elemen pada ts_a memenuhi syarat $\le$ terhadap ts_b, dengan setidaknya satu elemen bernilai lebih kecil. Hal ini membuktikan adanya ketergantungan kausalitas di mana event $a$ mendahului event $b$ secara kronologis.

2. Buat skenario di mana dua event concurrent (tidak ada yang precede yang lain) — tunjukkan dengan concurrent()
![image](https://hackmd.io/_uploads/ByVjFKsaZx.png)
Berdasarkan hasil simulasi, sistem berhasil mengidentifikasi konkurensi melalui fungsi concurrent() yang menghasilkan nilai True pada pengujian P2 dan P3. Hal ini terjadi karena secara teknis, vektor timestamp dari kedua proses tersebut tidak memiliki relasi "mendahului" (precede) satu sama lain; di mana salah satu vektor memiliki nilai lebih tinggi pada indeks tertentu namun lebih rendah pada indeks lainnya. Secara kausal, ini membuktikan bahwa kedua kejadian tersebut berlangsung secara independen tanpa adanya pertukaran informasi atau pesan di antara keduanya sebelum event tersebut tercatat, sehingga Vector Clock secara akurat mengklasifikasikannya sebagai kejadian yang berjalan paralel dalam sistem terdistribusi.

3. Bandingkan: apakah Lamport Clock bisa mendeteksi concurrency yang sama? 
![image](https://hackmd.io/_uploads/BJOatKsabl.png)
Lamport Clock tidak mampu mengidentifikasi konkurensi secara pasti seperti halnya Vector Clock. Keterbatasan ini muncul karena timestamp tunggal pada Lamport hanya bersifat linier; nilai $L(a) < L(b)$ tidak cukup kuat untuk membuktikan adanya dependensi kausalitas. Akibatnya, sistem tidak dapat memverifikasi apakah dua event tersebut saling memengaruhi atau justru bersifat konkuren, sehingga relasi happened-before ($\to$) tidak bisa dipastikan secara dua arah.

4. Tambah proses P3 yang mengirim pesan ke P1 secara bersamaan dengan P2 — gambar diagram vector clock-nya
![image](https://hackmd.io/_uploads/S1QFctjT-l.png)
![image](https://hackmd.io/_uploads/ry5P1ioTZg.png)

Dalam skenario ini, disimulasikan kondisi di mana proses P2 dan proses P3 bertindak secara independen dengan mengirimkan pesan ke proses P1 secara bersamaan tanpa adanya interaksi antar keduanya terlebih dahulu. Berdasarkan prinsip Vector Clock, kejadian pengiriman oleh P2 menghasilkan timestamp [0, 1, 0], sementara pengiriman oleh P3 menghasilkan [0, 0, 1]. Melalui perbandingan kedua vektor tersebut, sistem berhasil mendeteksi adanya konkurensi ($P2 \parallel P3$) karena tidak ada satu pun vektor yang mendominasi vektor lainnya secara keseluruhan. Proses sinkronisasi akhir terjadi pada P1, di mana setelah menerima kedua pesan tersebut, P1 menggabungkan seluruh informasi kausalitas yang ada menggunakan operasi nilai maksimal sehingga menghasilkan clock akhir [2, 1, 1]. Skenario ini membuktikan keunggulan Vector Clock dalam merekam sejarah kausalitas secara presisi, di mana status akhir P1 secara akurat mencerminkan kontribusi dari masing-masing proses yang berjalan secara paralel dan independen.