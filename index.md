```python
%store -r recent_launches
```

## Rachete, astronauți și sonde interplanetare
Siteul de față reprezintă o colecție personală de materiale, articole și notițe (mai mult sau mai puțin structurate) despre explorarea spațiului cosmic, adusă frecvent la zi și mereu extinsă, cu un accent pe rachete și lansări orbitale.

Știrile sunt grupate în Buletine Cosmice, distribuit sub formă de [newsletter](https://buletin.parsec.ro/) sau [podcast](https://www.anchor.fm/buletin).

## Ultimele lansări orbitale


```python
print(recent_launches)
```

    +----------+-----------------+---------------------+----------------------+------------------------------------------+----+--------------+
    | ID       | Date            | Rocket              | Series               | Sat * Mission                            | Or | LSite        |
    +----------+-----------------+---------------------+----------------------+------------------------------------------+----+--------------+
    | 2022-141 | 2022-10-28 0114 | Falcon 9 / FT5      | 184/B1063.8          | Starlink-67 (Starlink Group 4-31)        | US | VSFBS+SLC4E  |
    | 2022-140 | 2022-10-26 0020 | Soyuz-2-1A          | S 15000-057          | Progress MS-21 (Progress 7K-TGM No. 451) | RU | GIK-5+LC31   |
    | 2022-139 | 2022-10-22 1957 | Soyuz-2-1B / Fregat | Kh15000-011/ 142-503 | Skif-D/Gonets                            | RU | VOST+PU1S    |
    | 2022-138 | 2022-10-22 1837 | GSLV Mk III         | LVM3-M2              | OneWeb India-1 (OneWeb L14)              | IN | SHAR+SLP     |
    | 2022-137 | 2022-10-21 1900 | Soyuz-2-1V / Volga  | -                    | Kosmos-2561/2562 (14F164/14F172)         | RU | GIK-1+LC43/4 |
    | 2022-136 | 2022-10-20 1450 | Falcon 9 / FT5      | 183/B1062.10         | Starlink-66 (Starlink Group 4-36)        | US | CC+LC40      |
    | 2022-135 | 2022-10-15 1955 | Angara-1.2          | 71603?/2L            | Kosmos-2560 (EO MKA-3)                   | RU | GIK-1+LC35/1 |
    | 2022-134 | 2022-10-15 0522 | Falcon 9 / FT5      | 182/B1069.3          | Hot Bird 13F                             | US | CC+LC40      |
    | 2022-133 | 2022-10-14 1912 | Chang Zheng 2D      | Y69                  | YG-36 02 (Yaogan 36 02)                  | CN | XSC+LC3      |
    +----------+-----------------+---------------------+----------------------+------------------------------------------+----+--------------+
    

Detalii privind rachetele orbitale active:
- Statele Unite ale Americii: [Falcon 9](./r/falcon9.ipynb), [Falcon Heavy](./r/falconh.ipynb), [Atlas V](./r/atlasv.ipynb), Delta IV, Delta IV Heavy, Electron, Firefly Alhpa, LauncherOne, Astra, Antares, Minotaur, Pegasus
- China: CZ-2C, CZ-2D, CZ-2F, CZ-3B, CZ-3C, CZ-4B, CZ-4C, CZ-11, CZ-5, CZ-6, CZ-7, CZ-8, KZ-1A, KZ-11, Gushenxing-1, Lijian-1, Shuang Quxian 1, Jielong-1, OS-M1, Zhuque-1, KT-2
- Rusia: [Soyuz-2.1](./r/soyuz21.ipynb), [Soyuz-2.1v](./r/soyuz21v.ipynb), [Angara-1.2](./r/angara12.ipynb), [Proton-M](./r/protonm.ipynb), [Angara-A5](./r/angaraa5.ipynb)
- Europa: [Ariane 5](./r/ariane5.ipynb), [Vega-C](./r/vegac.ipynb)
- Japonia: [H-II], [Epsilon]
- India: [GSLV Mk. III](./r/gslvmk3.ipynb), [GSLV Mk. II](./r/gslvmk2.ipynb), [PSLV](./r/pslv.ipynb)
- Iran: Safir, Simorgh, Qased
- Israel: Shavit
- Coreea de Sud: Nuri
- Coreea de Nord: Kwangmyongsong


```python
!jupytext --to markdown index.ipynb
```

    [jupytext] Reading index.ipynb in format ipynb
    [jupytext] Executing notebook with kernel python3
    [jupytext] Updating the timestamp of index.md
    

    C:\Users\claud\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.9_qbz5n2kfra8p0\LocalCache\local-packages\Python39\site-packages\zmq\_future.py:679: RuntimeWarning: Proactor event loop does not implement add_reader family of methods required for zmq. Registering an additional selector thread for add_reader support via tornado. Use `asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())` to avoid this warning.
      self._get_loop()
    C:\Users\claud\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.9_qbz5n2kfra8p0\LocalCache\local-packages\Python39\site-packages\nest_asyncio.py:120: RuntimeWarning: Proactor event loop does not implement add_reader family of methods required for zmq. Registering an additional selector thread for add_reader support via tornado. Use `asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())` to avoid this warning.
      handle._run()
    


```python

```
